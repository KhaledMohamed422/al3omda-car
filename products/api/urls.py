from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.api.views import ProductViewSet, ProductDiscountViewSet, ProductImageListView

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('discounts', ProductDiscountViewSet, basename='discount')

urlpatterns = [
    path('', include(router.urls)),
    path('products/<int:product_id>/images/', ProductImageListView.as_view(), name='product-images'),
]
