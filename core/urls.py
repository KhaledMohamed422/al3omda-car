from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.api.shared.views import ProjectInfoRetrieveView

# Swagger
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="My API",
      default_version='v1',
      description="API documentation for all apps",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="support@example.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    
   # Project Information API
   path("", ProjectInfoRetrieveView.as_view(), name="project-info"),

   # Admin URLs 
   path("admin/", admin.site.urls),
   path('i18n/', include('django.conf.urls.i18n')),

   # App APIs
   path('api/orders/', include('orders.api.urls')),
   path('api/cart/', include('session_cart.api.urls')),
   path('api/products/', include('products.api.urls')),
   path('api/offers/', include('offers.api.urls')),
   path('api/shared/', include("core.api.shared.urls")),
   path('api/locations/', include('locations.api.urls')),

   # Swagger/OpenAPI Docs
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Serve media/static in dev
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
