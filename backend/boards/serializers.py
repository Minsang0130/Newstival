from rest_framework import serializers
from .models import Board
from django.contrib.auth.models import User

# 게시글 목록 Serializer (작성자를 닉네임으로 반환)
class BoardListSerializer(serializers.ModelSerializer):
    writer = serializers.SerializerMethodField()  # 작성자를 닉네임으로 변환

    class Meta:
        model = Board
        fields = ('id', 'title', 'content', 'writer',)
        read_only_fields = ('writer', )

    def get_writer(self, obj):
        # 작성자의 닉네임(username) 반환
        return obj.writer.username

# 게시글 상세 Serializer (작성자를 닉네임으로 반환)
class BoardSerializer(serializers.ModelSerializer):
    writer = serializers.SerializerMethodField()  # 작성자를 닉네임으로 변환

    class Meta:
        model = Board
        fields = '__all__'

    def get_writer(self, obj):
        # 작성자의 닉네임(username) 반환
        return obj.writer.username
