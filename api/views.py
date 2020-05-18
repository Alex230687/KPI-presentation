from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import IndicatorLongDetailSerializer
from main.models import Indicator


class IndicatorLongDetailView(APIView):
    """
    View for detail indicator information.
    Get from URL indicator id and year for Report model filter.
    """
    def get(self, request, id, year):
        indicator = Indicator.objects.prefetch_related('report_set', 'scale_set').get(id=id)
        serializer = IndicatorLongDetailSerializer(indicator, context={'id': id, 'year': year})
        return Response(serializer.data)
