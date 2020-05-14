from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Indicator
from .serializers import IndicatorLongDetailSerializer


class IndicatorLongDetailView(APIView):
    def get(self, request, id, year):
        indicator = Indicator.objects.prefetch_related('report_set', 'scale_set').get(id=id)
        serializer = IndicatorLongDetailSerializer(indicator, context={'id': id, 'year': year})
        return Response(serializer.data)
S