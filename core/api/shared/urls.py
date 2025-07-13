from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, TruckTypeViewSet, CountryViewSet, ProjectInfoRetrieveUpdateView
from django.urls import path

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'trucks', TruckTypeViewSet)
router.register(r'countries', CountryViewSet)

urlpatterns = router.urls + [
    path("project-info/", ProjectInfoRetrieveUpdateView.as_view(), name="project-info"),
]
