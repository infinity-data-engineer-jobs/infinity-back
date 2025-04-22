from django.shortcuts import render, redirect
from .models import NoticeInfo, CompanyInfo
from .serializers import NoticeInfoSerializer, CompanyInfoSerializer
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Q,F
from wentedCrawl.transform import transform_tech
from django.http import JsonResponse
import re

#index 페이지 view
def index(request):
    return render(request, 'index.html')
#기술 스택 차트 view
def techStackChart(request):
    return render(request, 'charts/techStackChart.html')

#기술 스택 워드클라우드 view
def techStackWordCloud(request):
    return render(request, 'charts/techStackWordCloud.html')

#연봉/인원수 별 기술 스택 분포 차트 view
def revenueTechStacks(request):
    return render(request, 'charts/revenueTechStacks.html')

#회사 규모 차트 view
def companyScalesChart(request):
    return render(request, 'charts/companyScalesChart.html')


#우대사항 차트 view
def preferredQualificationChart(request):
    return render(request, 'charts/preferredQualificationChart.html')

#주요업무 차트 view
def mainWorkChart(request):
    return render(request, 'charts/mainWorkChart.html')

# 공고 정보 전체 조회
def transform_data(request):
    transform_tech.transform_to_techstack()
    return redirect('/')

class NoticeInfoViewSet(generics.ListAPIView):
    queryset = NoticeInfo.objects.all()
    serializer_class = NoticeInfoSerializer
# 회사 정보 전체 조회
class CompanyInfoViewSet(generics.ListAPIView):
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer

# 차트 관련 원천 데이터 조회
class NoticeTeckStckInfoViewSet(generics.ListAPIView):
    queryset = CompanyInfo.objects.filter(
        Q(company_headcount__regex=r'^\d+$') &  # company_headcount가 숫자로만 이루어진 경우
        Q(notices__notice_tech_stack__isnull=False)  # notices의 notice_tech_stack이 null이 아닌 경우
    ).annotate(
        notice_id=F('notices__notice_id'),
        notice_tech_stack=F('notices__notice_tech_stack'),
        notice_title=F('notices__notice_title'),
        notice_location=F('notices__notice_location')
    ).values(
        'company_id', 
        'company_name', 
        'company_headcount', 
        'company_salary',
        'company_revenue',
        'notice_id', 
        'notice_tech_stack', 
        'notice_title', 
        'notice_location'
    )
    serializer_class = None  # values()를 사용하면 serializer가 필요 없음

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # company_revenue 값을 정수형으로 변환
        def parse_revenue(revenue):
            if not revenue:  # None 또는 빈 문자열 처리
                return 0
            if '억원' in revenue:
                return int(float(revenue.replace('억원', '').strip()) * 100000000)
            elif '만원' in revenue:
                return int(float(revenue.replace('만원', '').strip()) * 10000)
            return 0  # 변환할 수 없는 경우 기본값

        # 데이터 가공
        processed_data = []
        for item in queryset:
            item['company_revenue'] = parse_revenue(item.get('company_revenue'))
            processed_data.append(item)
        
        return Response(processed_data)  # 데이터를 JSON으로 반환


# company_headcount 문자열에서 숫자만 추출하는 파서
def parse_headcount(raw):
    if not raw:
        return None
    digits = re.sub(r'[^0-9]', '', str(raw))
    try:
        return int(digits) if digits else None
    except:
        return None

# company_headcount 범주화 + 개수 카운트
def company_headcount_distribution(request):
    queryset = CompanyInfo.objects.values_list('company_headcount', flat=True)

    # 범주 구간 정의
    ranges = [
        (0, 200),
        (200, 400),
        (400, 600),
        (600, 800),
        (800, 1000),
        (1000, 1200)
    ]
    bins = {f"{start}~{end}": 0 for start, end in ranges}
    bins["1200 이상"] = 0

    for raw in queryset:
        headcount = parse_headcount(raw)
        if headcount is None:
            continue
        found = False
        for start, end in ranges:
            if start <= headcount < end:
                bins[f"{start}~{end}"] += 1
                found = True
                break
        if not found:
            bins["1200 이상"] += 1

    return JsonResponse(bins)
    