from rest_framework import generics
from core.models.shared import Category, TruckType, Country
from core.models.project_info import ProjectInfo
from .serializers import (
    CategorySerializer,
    TruckTypeSerializer,
    CountrySerializer,
    ProjectInfoSerializer,
)

# ------------------------------------------------------------------------------
# Shared Data (List-Only Views)
# ------------------------------------------------------------------------------
class CategoryListView(generics.ListAPIView):
    """
    GET only: returns all categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TruckTypeListView(generics.ListAPIView):
    """
    GET only: returns all truck types.
    """
    queryset = TruckType.objects.all()
    serializer_class = TruckTypeSerializer


class CountryListView(generics.ListAPIView):
    """
    GET only: returns all countries.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


# ------------------------------------------------------------------------------
# Project Information
# ------------------------------------------------------------------------------
class ProjectInfoRetrieveView(generics.RetrieveAPIView):
    """
    Retrieve the single ProjectInfo instance (singleton pattern).
    """
    serializer_class = ProjectInfoSerializer

    def get_object(self):
        return ProjectInfo.objects.first()
