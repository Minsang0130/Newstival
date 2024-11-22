# festivals_news/urls.py
from django.urls import path
from .views import FilterNewsByRegion

urlpatterns = [
    # 지역 필터 API 엔드포인트
    path('region/<str:region>/', FilterNewsByRegion.as_view(), name='filter-news-by-region'),
]
