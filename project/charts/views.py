from django.shortcuts import render, redirect
from .models import NoticeInfo, CompanyInfo
from .serializers import NoticeInfoSerializer, CompanyInfoSerializer
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Q,F
from wentedCrawl.transform import transform_tech

def index(request):
    return render(request, 'index.html')

def transform_data(request):
    transform_tech.transform_to_techstack()
    return redirect('/')

class NoticeInfoViewSet(generics.ListAPIView):
    queryset = NoticeInfo.objects.all()
    serializer_class = NoticeInfoSerializer

class CompanyInfoViewSet(generics.ListAPIView):
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer

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


