# backend/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('boards.urls')),  # 기존 boards 앱 경로
    path('api/news/', include('festivals_news.urls')),  # festivals_news 앱의 URL 패턴 추가
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
]
