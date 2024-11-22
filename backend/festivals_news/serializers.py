# festivals_news/serializers.py
from rest_framework import serializers
from .models import FestivalNews

class FestivalNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FestivalNews
        fields = ['id', 'festival_name', 'title', 'originallink', 'link', 'description', 'pub_date', 'main_region']
