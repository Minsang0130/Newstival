# festivals_news/models.py
from django.db import models

class FestivalNews(models.Model):
    festival_name = models.CharField(max_length=255)
    title = models.CharField(max_length=500)
    originallink = models.URLField(max_length=500)
    link = models.URLField(unique=True, max_length=500)  # 중복 제거를 위해 unique 설정
    description = models.TextField(blank=True)
    pub_date = models.DateTimeField()
    main_region = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title
