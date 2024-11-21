from django.db import models

class Festival_Details(models.Model):
    title = models.CharField(max_length=255, verbose_name="축제 이름")
    region = models.CharField(max_length=255, null=True, blank=True, verbose_name="지역")
    period = models.CharField(max_length=255, null=True, blank=True, verbose_name="기간")
    nature = models.CharField(max_length=255, null=True, blank=True, verbose_name="축제 성격")
    fee = models.CharField(max_length=255, null=True, blank=True, verbose_name="입장료")
    info = models.TextField(null=True, blank=True, verbose_name="추가 정보")
    url = models.URLField(null=True, blank=True, verbose_name="상세 페이지 URL")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")

    def __str__(self):
        return self.title
