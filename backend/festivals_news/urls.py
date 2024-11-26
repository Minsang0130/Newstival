# festivals_news/urls.py
from django.urls import path
from .views import NewsByRegionView, AllNewsView, TopRegionsView
from . import views

urlpatterns = [
    # 지역 필터 API 엔드포인트
    path('region/<str:region>/', NewsByRegionView.as_view(), name='news-by-region'),
    path('', AllNewsView.as_view(), name='all-news'),
    path('wordcloud/<str:region>/', views.get_wordcloud_data, name='get_wordcloud_data'),
    path('heatmap/', views.get_heatmap_data),
    path('top-regions/', TopRegionsView.as_view(), name='top-regions'),
    path('chatbot/', views.chatbot_api, name='chatbot_api'),
]
