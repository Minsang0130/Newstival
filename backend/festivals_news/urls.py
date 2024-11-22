# festivals_news/urls.py
from django.urls import path
from .views import FilterNewsByRegion

urlpatterns = [
    # 지역 필터 API 엔드포인트
    path('region/<str:region>/', FilterNewsByRegion.as_view(), name='filter-news-by-region'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('wordcloud/', views.get_wordcloud_data, name='get_wordcloud_data'),
]
