from django.shortcuts import render
from django.http import JsonResponse
from collections import Counter
import re
from .models import FestivalNews
from bs4 import BeautifulSoup
import html
from django.db.models import Count
from datetime import datetime

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
        # 로그 출력
        print(f"Requested region: {region}")
        # 데이터베이스에서 해당 지역의 뉴스 검색
        articles = FestivalNews.objects.filter(main_region=region)
        if not articles.exists():
            # 지역에 해당하는 뉴스가 없는 경우
            return Response(
                {"error": f"No articles found for region: {region}"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = FestivalNewsSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



def decode_html_entities(text):
    return html.unescape(text)

def clean_html_keep_important(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()  # 중요 내용은 유지하고 HTML 태그만 제거

def get_wordcloud_data(request):
    region = request.GET.get('region', 'all')  # "all"이 기본값

    # 지역별 데이터 필터링
    if region != 'all':
        news_queryset = FestivalNews.objects.filter(festival_name__icontains=region)
    else:
        news_queryset = FestivalNews.objects.all()

    # 뉴스 기사 내용을 모두 결합
    all_text = " ".join(news_queryset.values_list("description", flat=True))

    # 간단한 텍스트 정리: 특수문자 제거, 소문자 변환, HTML 태그 제거
    cleaned_text = clean_html_keep_important(all_text)  # HTML 태그 제거
    cleaned_text = decode_html_entities(cleaned_text)  # HTML 엔티티 디코딩

    # 단어 분리 및 필터링: 소문자로 변환하여 단어만 추출
    words = re.findall(r'\b[a-zA-Z가-힣]+\b', cleaned_text.lower())

    # 단어 빈도 계산
    word_counts = Counter(words)

    # 빈도 높은 단어를 상위 100개로 제한
    wordcloud_data = word_counts.most_common(100)

    return JsonResponse(wordcloud_data, safe=False)

def get_heatmap_data(request):
    # 오늘 날짜 기준으로 뉴스 개수를 계산
    today = datetime.now()
    news_queryset = FestivalNews.objects.filter(pub_date__date=today)

    # 지역별로 그룹화하고 개수를 세기
    region_counts = news_queryset.values('main_region').annotate(count=Count('id'))

    # JsonResponse로 변환하여 반환
    return JsonResponse(list(region_counts), safe=False)
