from django.contrib import admin
from django.urls import path, include
# from boards import views

# 개발 서버 기본 경로: http://127.0.0.1:8000/
urlpatterns = [
    path('admin/', admin.site.urls),    
    path('api/v1/', include('boards.urls')),
    path('dashboard/', include('festivals_news.urls')),

    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
]
