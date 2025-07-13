from django.urls import path
from .views import (
    CartView, CartAddView, CartUpdateView,
    CartRemoveView, CartTotalView, CartCountView
)

urlpatterns = [
    path('', CartView.as_view(), name='cart-detail'),
    path('add/', CartAddView.as_view(), name='cart-add'),
    path('update/', CartUpdateView.as_view(), name='cart-update'),
    path('remove/', CartRemoveView.as_view(), name='cart-remove'),
    path('total/', CartTotalView.as_view(), name='cart-total'),
    path('count/', CartCountView.as_view(), name='cart-count'),
]
