from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Category, Product, ProductImage, ProductVariation, Cart, CartItem 
from .serializers import ProductVariationSerializer, ProductVariationSerializer, ProductSerializer, CategorySerializer, CartSerializer, CartItemSerializer

class ProductView(APIView):
  serializer_class = ProductSerializer
  # permission_classes = [IsAuthenticated]

  def post(self,requst):
    serializer = self.serializer_class(data=requst.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      return Response({'Message':'Product created successfully'},status=status.HTTP_200_OK)