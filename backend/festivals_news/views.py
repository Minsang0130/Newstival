from django.shortcuts import render

# Create your views here.

# festivals_news/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FestivalNews
from .serializers import FestivalNewsSerializer

# 지역에 해당하는 뉴스를 필터링하여 반환하는 API
class FilterNewsByRegion(APIView):
    def get(self, request, region):
        # main_region이 주어진 지역과 일치하는 뉴스 필터링
        articles = FestivalNews.objects.filter(main_region=region)
        
        # 직렬화하여 반환
        serializer = FestivalNewsSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
