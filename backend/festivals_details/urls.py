from django.urls import path
from .views import EventByRegionView

urlpatterns = [
    path('events/region/<str:region>/', EventByRegionView.as_view(), name='events-by-region'),
]
