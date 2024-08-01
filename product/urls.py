from django.urls import path
from .views import ProductView, ProductDetailsView, ProductImageView, CartItemView


urlpatterns = [
  path('products/', ProductView.as_view(), name='product-list'),
  path('products/<str:pk>/', ProductDetailsView.as_view(), name='product-detail'),
  path('products/<str:pk>/images/',ProductImageView.as_view(), name='products-images'),
  path('cart-items/', CartItemView.as_view(), name='cart-item-list'),
]