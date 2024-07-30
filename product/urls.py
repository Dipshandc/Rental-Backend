from django.urls import path
from .views import ProductView 


urlpatterns = [
  path('list_product/',ProductView.as_view(),name='Product endpoint'),
]