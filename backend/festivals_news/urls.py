# festivals_news/urls.py
from django.urls import path
from .views import NewsByRegionView
from .views import AllNewsView
from . import views

urlpatterns = [
    # 지역 필터 API 엔드포인트
    path('region/<str:region>/', NewsByRegionView.as_view(), name='news-by-region'),
    path('', AllNewsView.as_view(), name='all-news'),
    path('wordcloud/', views.get_wordcloud_data, name='get_wordcloud_data'),
    path('heatmap/', views.get_heatmap_data),
]
