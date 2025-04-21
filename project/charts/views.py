from django.shortcuts import render
from .models import NoticeInfo, CompanyInfo
from .serializers import NoticeInfoSerializer, CompanyInfoSerializer
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Q,F

def index(request):
    return render(request, 'index.html')

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
        'notice_id', 
        'notice_tech_stack', 
        'notice_title', 
        'notice_location'
    )
    serializer_class = None  # values()를 사용하면 serializer가 필요 없음

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return Response(list(queryset))  # 데이터를 JSON으로 반환


