from rest_framework.response import Response
from rest_framework import filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product, ProductImage, ProductVariation, Cart, CartItem 
from .filters import ProductFilter
from .serializers import ProductVariationSerializer,\
                         ProductSerializer,\
                         CategorySerializer,\
                         CartSerializer,\
                         CartItemSerializer

class ProductPagination(PageNumberPagination):
    page_size = 20

class ProductView(APIView):
  serializer_class = ProductSerializer
  # permission_classes = [IsAuthenticated]
  search_fields = ['name','category','description']
  filter_backends = (filters.SearchFilter,DjangoFilterBackend)
  filterset_class = ProductFilter

  def get(self,request):
    product = Product.objects.all()
    paginator = ProductPagination()
    paginated_product = paginator.paginate_queryset(product, request)
    serializer = self.serializer_class(paginated_product,many=True)
    return paginator.get_paginated_response(serializer.data)

  def post(self,request):
    serializer = self.serializer_class(data=request.data,context={'user': request.user})
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      return Response({'Message':'Product created successfully'},status=status.HTTP_200_OK)

