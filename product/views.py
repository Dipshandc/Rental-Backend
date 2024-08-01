from rest_framework.response import Response
from rest_framework import filters, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes as method_permission_classes
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product, ProductImage, ProductVariation, Cart, CartItem, ProductVariation
from .filters import ProductFilter
from .serializers import ProductVariationSerializer,\
                         ProductSerializer,\
                         RecursiveCategorySerializer,\
                         CartItemSerializer,\
                         ProductImageSerializer


class ProductPagination(PageNumberPagination):
    page_size = 20


class ProductView(APIView):
  serializer_class = ProductSerializer
  permission_classes = [AllowAny]
  search_fields = ['name','category','description']
  filter_backends = (filters.SearchFilter,DjangoFilterBackend)
  filterset_class = ProductFilter

  def get(self,request):
    product = Product.objects.all()
    paginator = ProductPagination()
    paginated_product = paginator.paginate_queryset(product, request)
    serializer = self.serializer_class(paginated_product,many=True)
    return paginator.get_paginated_response(serializer.data)

  @method_permission_classes([IsAuthenticated])
  def post(self,request):
    serializer = self.serializer_class(data=request.data,context={'user': request.user})
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      return Response({'Message':'Product created successfully'},status=status.HTTP_200_OK)


class ProductDetailsView(APIView):
  serializer_class = ProductSerializer
  permission_classes = [AllowAny]

  def get(self,request,pk):
    product = get_object_or_404(Product,id=pk)
    serializer = self.serializer_class(product)
    return Response(serializer.data,status=status.HTTP_200_OK)
  
  @method_permission_classes([IsAuthenticated])
  def patch(self,request,pk):
    product = get_object_or_404(Product,pk=pk)
    serializer = self.serializer_class(product,data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      return Response({'Message':'Product updated successfully'},status=status.HTTP_200_OK)
  
  def delete(self,request,pk):
    product = get_object_or_404(Product,pk=pk)
    if product.user == request.user:
      product.delete()
      return Response({'Message':'Product deleted successfully'},status=status.HTTP_200_OK)
    else:
      return Response({'Message':'You are not authorized to delete this product'},status=status.HTTP_403_FORBIDDEN)


class CartItemView(APIView):
  serializer_class = CartItemSerializer
  permission_classes = [IsAuthenticated]

  def get(self,request):
    cart = get_object_or_404(Cart,user=request.user)
    cart_item = CartItem.objects.fileter(cart=cart)
    serializer = self.serializer_class(cart_item,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)
  
  def patch(self,request):
    cart = get_object_or_404(Cart,user=request.user)
    cart_items_data = request.data
    updated_items = []
    for item_data in cart_items_data:
      cart_item = CartItem.objects.filter(cart=cart, product=item_data.product).first()
      if not cart_item:
        continue
      serializer = self.serializer_class(cart_item, data=item_data, partial=True)
      if serializer.is_valid(raise_exception=True):
        serializer.save()
        updated_items.append(serializer.data)
      return Response({'Message': 'Cart updated successfully', 'updated_items': updated_items}, status=status.HTTP_200_OK)


class ProductImageView(APIView):
  serializer_class = ProductImageSerializer
  permission_classes = [AllowAny]

  def get(self,request,pk):
    product = get_object_or_404(Product,pk=pk)
    product_images = ProductImage.objects.filter(product=product)
    serializer = self.serializer_class(product_images,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)
  
  @method_permission_classes([IsAuthenticated])
  def post(self,request,pk):
    product = get_object_or_404(Product,pk=pk)
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save(product=product)
      return Response({'Message':'Product image added'},status=status.HTTP_201_CREATED)


class ProductVariationView(APIView):
  serializer_class = ProductVariationSerializer
  permission_classes = [AllowAny]

  def get(self,request,pk):
    product = get_object_or_404(Product,pk=pk)
    product_variations = get_object_or_404(ProductVariation,product=product)
    serializer = self.serializer_class(product_variations,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)
  
  @method_permission_classes([IsAuthenticated])
  def post(self,request,pk):
    product = get_object_or_404(Product,pk=pk)
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save(product=product)
      return Response({'Message':'Product veriation added'},status=status.HTTP_201_CREATED)

  @method_permission_classes([IsAuthenticated])
  def patch(self,request,pk):
    product = get_object_or_404(Product,pk=pk)
    product_variations = get_object_or_404(ProductVariation,product=product)
    serializer = self.serializer_class(product_variations,data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      return Response({'Message':'Product veriation edited successfully'},status=status.HTTP_201_CREATED)
    

class NestedCategoryListView(APIView):
  def get(self, request):
    root_categories = Category.objects.filter(parent=None)
    serializer = RecursiveCategorySerializer(root_categories, many=True)
    return Response(serializer.data)