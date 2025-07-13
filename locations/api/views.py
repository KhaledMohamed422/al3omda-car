from rest_framework import viewsets
from locations.models import Governorate, City
from .serializers import GovernorateSerializer, CitySerializer


class GovernorateViewSet(viewsets.ModelViewSet):
    queryset = Governorate.objects.all()
    serializer_class = GovernorateSerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
