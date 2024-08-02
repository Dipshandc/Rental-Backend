from django.urls import path
from .views import ProductView,\
                   ProductDetailsView,\
                   ProductImageView,\
                   CartItemView,\
                   ProductVariationView,\
                   NestedCategoryListView,\
                   LikeProductView,\
                   LikedProductsView


urlpatterns = [
  path('products/', ProductView.as_view(), name='product-list'),
  path('products/<str:pk>/', ProductDetailsView.as_view(), name='product-detail'),
  path('products/<str:pk>/images/',ProductImageView.as_view(), name='products-images'),
  path('products/<str:pk>/variation/',ProductVariationView.as_view(), name='products-variation'),
  path('category/',NestedCategoryListView.as_view(), name='category'),
  path('cart-items/', CartItemView.as_view(), name='cart-item-list'),
  path('products/<int:pk>/like/', LikeProductView.as_view(), name='like-product'),
  path('products/liked/', LikedProductsView.as_view(), name='liked-products'),
]