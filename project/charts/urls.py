from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name="index"),
    path('/', views.index,name="index"),
    path('techStackChart/', views.techStackChart,name="techStackChart"),
    path('techStackWordCloud/', views.techStackWordCloud,name="techStackWordCloud"),
    path('revenueTechStacks/', views.revenueTechStacks,name="revenueTechStacks"),
    path('companyScalesChart/', views.companyScalesChart,name="companyScalesChart"),
    path('mainWorkChart/', views.mainWorkChart, name="mainWorkChart"),
    path('mainWorkChartData/', views.main_work_chart_data, name="mainWorkChartData"),  # 라벨 데이터 API
    path('preferredQualificationChart/', views.preferredQualificationChart,name="preferredQualificationChart"),
    path('preferred-qualification/', views.PreferredQualificationInfoViewSet.as_view(), name='preferredQualification'),
    path('company/', views.CompanyInfoViewSet.as_view(),name="companyInfo"),
    path('notice/', views.NoticeInfoViewSet.as_view(),name="noticeInfo"),
    path('notice/techstack/', views.NoticeTeckStckInfoViewSet.as_view(),name="noticeTechStack"),
    path('transform/', views.transform_data, name="transform_data"),
    path('api/headcount-distribution/', views.company_headcount_distribution, name='headcountDistribution')
]
