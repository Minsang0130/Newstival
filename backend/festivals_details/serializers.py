from rest_framework import serializers
from festivals_details.models import Festival_Details

class FestivalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Festival_Details
        fields = '__all__'
