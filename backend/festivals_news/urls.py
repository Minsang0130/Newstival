from django.urls import path
from . import views

urlpatterns = [
    path('wordcloud/', views.get_wordcloud_data, name='get_wordcloud_data'),
    path('heatmap/', views.get_heatmap_data),
]
