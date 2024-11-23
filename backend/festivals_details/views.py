from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from festivals_details.models import Festival_Details
from festivals_details.serializers import FestivalDetailsSerializer

class EventByRegionView(APIView):
    """
    선택한 지역에 따라 관련 행사 정보를 반환합니다.
    선택한 지역이 없을 경우 모든 축제 정보를 반환합니다.
    """
    def get(self, request, region=None):
        if region:
            events = Festival_Details.objects.filter(Main_Region=region)
            if not events.exists():
                return Response({"message": f"No events found for region: {region}"}, status=status.HTTP_404_NOT_FOUND)
        else:
            events = Festival_Details.objects.all()  # 모든 축제 정보를 반환

        serializer = FestivalDetailsSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)