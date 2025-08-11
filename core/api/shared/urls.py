from django.urls import path
from .views import (
    CategoryListView,
    TruckTypeListView,
    CountryListView,
    ProjectInfoRetrieveView
)

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="categories"),
    path("truck-types/", TruckTypeListView.as_view(), name="truck-types"),
    path("countries/", CountryListView.as_view(), name="countries"),
    path("project-info/", ProjectInfoRetrieveView.as_view(), name="project-info"),
]
