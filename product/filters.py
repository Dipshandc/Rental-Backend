from django_filters import FilterSet 
from .models import Product

class ProductFilter(FilterSet):
  class Meta:
    model = Product
    fields = {
      'location':['exact'],
      'category':['exact',],
      'price':['lte','gte'],
    }