from django.urls import path
from .views import EventByRegionView

urlpatterns = [
    path('events/', EventByRegionView.as_view(), name='all-events'),  # 모든 축제 정보
    path('events/region/<str:region>/', EventByRegionView.as_view(), name='events-by-region'),
]
