from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from locations.models import Governorate, City
from .serializers import GovernorateSerializer, CitySerializer


class GovernorateViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    """
    GET-only API for governorates.
    """
    queryset = Governorate.objects.all()
    serializer_class = GovernorateSerializer

    @action(detail=True, methods=['get'], url_path='cities')
    def cities(self, request, pk=None):
        """
        Get all cities for a given governorate.
        """
        governorate = self.get_object()
        cities = governorate.cities.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)
