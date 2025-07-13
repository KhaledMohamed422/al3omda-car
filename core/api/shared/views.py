from rest_framework import viewsets
from core.models.shared import Category, TruckType, Country
from .serializers import CategorySerializer, TruckTypeSerializer, CountrySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TruckTypeViewSet(viewsets.ModelViewSet):
    queryset = TruckType.objects.all()
    serializer_class = TruckTypeSerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


from rest_framework import generics
from core.models.project_info import ProjectInfo
from .serializers import ProjectInfoSerializer

class ProjectInfoRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ProjectInfoSerializer

    def get_object(self):
        return ProjectInfo.objects.first()  # Always return the singleton instance

