#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import json
import time
import django
import openai
from tqdm import tqdm
from django.db import connection, transaction
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# ——— 한글 폰트 설정 ———
font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
if os.path.exists(font_path):
    font_prop = font_manager.FontProperties(fname=font_path)
    rc('font', family=font_prop.get_name())
else:
    rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

# ① Django 환경 셋업
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # project/ 폴더
sys.path.append(BASE_DIR)                              # manage.py가 있는 폴더
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wentedCrawl.settings")
django.setup()


# ② GPT 호출 및 그룹화 함수들
def split_sentences(text):
    return re.split(r'[•\-\n\.]+', text)


def call_gpt_analysis(text_list, api_key,
                      model_name="gpt-4o", max_tokens_per_batch=12000):
    client = openai.OpenAI(api_key=api_key)
    batches, current, toks = [], [], 0

    def estimate_tokens(txt):
        return int(len(txt.split()) * 1.5)

    # 배치 분할
    for s in text_list:
        t = estimate_tokens(s)
        if toks + t >= max_tokens_per_batch:
            batches.append(current); current = []; toks = 0
        current.append(s); toks += t
    if current: batches.append(current)

    merged = []
    for batch in tqdm(batches, desc="1) GPT 그룹화"):
        prompt = f"""
아래 문장 리스트를 대주제(headline) 수준으로 포괄적인 대표 문장 하나와,
그 그룹에 속하는 모든 문장들을 포함하는 리스트를 출력해주세요.
즉, 대표 문장은 “그룹 내 모든 문장들의 공통 주제”를 넓게 아우르는 한 줄 짜리 헤드라인이어야 합니다.
각 그룹에 대해 다음 필드를 가지는 JSON 배열을 리턴해주세요:
  - representative_sentence: 포괄적인 한 문장 헤드라인
  - frequency: 그룹 내 문장 수
  - sentences: 그룹에 속하는 모든 원문 문장 리스트

문장 리스트:
{batch}

(반드시 ```json ... ``` 안에 JSON만 리턴)
"""
        # 최대 3회 재시도
        for _ in range(3):
            try:
                resp = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role":"system", "content":"You are a helpful assistant that analyzes and groups similar sentences."},
                        {"role":"user",   "content":prompt},
                    ],
                )
                content = resp.choices[0].message.content
                # ```json ... ``` 추출
                if '```json' in content:
                    js = content.split('```json')[1].split('```')[0]
                else:
                    js = content[content.index('{'):content.rindex('}')+1]
                merged.append(json.loads(js))
                break
            except Exception:
                time.sleep(30)

    # 결과 병합
    result = {}
    for group in merged:
        for e in group:
            rep = e['representative_sentence']
            if rep in result:
                result[rep]['frequency'] += e['frequency']
                result[rep]['sentences'].extend(e['sentences'])
            else:
                result[rep] = e
    return result, len(batches)


def regroup_representatives(reps, api_key, model="gpt-4o"):
    prompt = f"""
다음은 우대사항 대표 문장 리스트입니다.
의미가 비슷한 것끼리 상위 그룹으로 묶어주세요.
결과는 JSON: key=상위 대표문장, value=하위 대표문장 리스트

{reps}
"""
    client = openai.OpenAI(api_key=api_key)
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role":"system", "content":"You merge similar categories."},
            {"role":"user",   "content":prompt},
        ],
    )
    content = resp.choices[0].message.content
    if '```json' in content:
        js = content.split('```json')[1].split('```')[0]
    else:
        js = content[content.index('{'):content.rindex('}')+1]
    return json.loads(js)


def build_final_groups(merged, regroup_map):
    final = {}
    for top, children in regroup_map.items():
        freq, sents = 0, []
        for rep in children:
            if rep in merged:
                freq += merged[rep]['frequency']
                sents.extend(merged[rep]['sentences'])
        final[top] = {
            'representative_sentence': top,
            'frequency': freq,
            'sentences': sents
        }
    return final


# ③ 실제 처리 로직
def main():
    # OpenAI 키 (환경변수)
    API_KEY = os.getenv("OPENAI_API_KEY")
    if not API_KEY:
        print("❌ 환경변수 OPENAI_API_KEY가 설정되어 있지 않습니다.")
        return

    # 1) DB에서 우대사항 텍스트 로드
    from charts.models import NoticeInfo
    qs = NoticeInfo.objects \
        .exclude(notice_preferred_qualification__isnull=True) \
        .values_list('notice_preferred_qualification', flat=True)

    sentences = []
    for txt in qs:
        for s in split_sentences(txt):
            s = s.strip()
            if len(s) > 1:
                sentences.append(s)

   # 2) 1차 GPT 그룹화 & 병합 (배치 수도 반환)
    merged, batch_count = call_gpt_analysis(sentences, API_KEY)

    # 3) 배치가 1개일 경우, 재그룹핑 없이 final=merged
    if batch_count > 1:
        reps = list(merged.keys())
        regroup_map = regroup_representatives(reps, API_KEY)
        final = build_final_groups(merged, regroup_map)
    else:
        final = merged

    # 4) DB 테이블 생성(없으면) 및 INSERT
    with connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS charts_preferred_qualificationinfo;")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS charts_preferred_qualificationinfo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            representative_sentence TEXT NOT NULL,
            frequency INTEGER NOT NULL,
            sentences TEXT
        );
        """)
        for info in final.values():
            rep   = info['representative_sentence']
            freq  = info['frequency']
            sents = "|".join(info['sentences'])
            cursor.execute("""
            INSERT INTO charts_preferred_qualificationinfo
                (representative_sentence, frequency, sentences)
            VALUES (%s, %s, %s)
            """, [rep, freq, sents])
        transaction.commit()

    print(f"✅ {len(final)}개 그룹을 charts_preferred_qualificationinfo 테이블에 저장했습니다.")


if __name__ == "__main__":
    main()
