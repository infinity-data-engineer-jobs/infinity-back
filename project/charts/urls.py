from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name="index"),
    path('/', views.index,name="index"),
    path('company/', views.CompanyInfoViewSet.as_view(),name="companyInfo"),
    path('notice/', views.NoticeInfoViewSet.as_view(),name="noticeInfo"),
    path('notice/techstack/', views.NoticeTeckStckInfoViewSet.as_view(),name="noticeTechStack"),
]
