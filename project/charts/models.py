from django.db import models

# 회사 정보
class CompanyInfo(models.Model):
    company_id = models.IntegerField(null=False,primary_key=True)   #회사PK
    company_name = models.CharField(null=True)                      #회사명
    company_tag = models.CharField(null=True)                       #태그
    company_salary = models.CharField(null=True)                    #연봉
    company_location = models.CharField(null=True)                  #위치
    company_headcount = models.CharField(null=True)                 #인원
    company_revenue = models.CharField(null=True)                   #매출
    company_info = models.CharField(null=True)                      #기업 정보 (없을수 있음)
    reg_dt = models.DateTimeField(auto_now_add=True)                #등록일시
    mod_dt = models.DateTimeField(auto_now_add=True)                #수정일시

# 공고 정보
class NoticeInfo(models.Model):
    notice_id = models.IntegerField(primary_key=True)               #공고PK
    company_id = models.ForeignKey(CompanyInfo,db_column='company_id',related_name='notices',on_delete=models.CASCADE) #회사PK
    notice_job_category = models.CharField(null=True)               #직무분야
    notice_location = models.CharField(null=True)                   #근무지
    notice_career = models.CharField(null=True)                     #경력사항
    notice_title = models.CharField(null=True)                      #공고제목
    notice_position = models.CharField(null=True)                   #포지션상세
    notice_main_work = models.CharField(null=True)                  #주요업무
    notice_qualification = models.CharField(null=True)              #자격요건
    notice_preferred_qualification = models.CharField(null=True)    #우대사항
    notice_welfare = models.CharField(null=True)                    #혜택 및 복지
    notice_category = models.CharField(null=True)                   #채용 전형
    notice_end_date = models.CharField(null=True)                   #마감일
    notice_tech_stack = models.CharField(null=True)                 #기술 스택 • 툴 (없을수 있음)
    notice_url = models.CharField(null=True)                        #공고URL
    reg_dt = models.DateTimeField(auto_now_add=True)                #등록일시
    mod_dt = models.DateTimeField(auto_now_add=True)                #수정일시

# 우대사항 정보
class PreferredQualificationInfo(models.Model):
    representative_sentence = models.CharField(null=True)          #대표 문장
    frequency = models.IntegerField(null=True)                      #빈도
    sentences = models.TextField(null=True)                         #문장 리스트
    class Meta:
            db_table = "charts_preferred_qualificationinfo"


class MainWorkChart(models.Model):
    # row_id = models.IntegerField(db_column='id')                    #주요업무 행번호PK
    notice_id = models.IntegerField()                                #공고ID
    notice_main_work = models.TextField(db_column="main_work")       #주요업무
    label = models.IntegerField()

    class Meta:
        db_table = 'charts_mainwork'  # 테이블 이름 설정

