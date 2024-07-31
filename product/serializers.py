from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Product, Category, ProductImage, ProductVariation, Cart, CartItem

class ProductVariationSerializer(ModelSerializer):
  class Meta:
    model = ProductVariation
    fields = ['name','price','stock']

class ProductImageSerializer(ModelSerializer):
  class Meta:
    model = ProductImage
    fields = ['image','alt_text']

class ProductSerializer(ModelSerializer):
  variations = ProductVariationSerializer(many=True, read_only=True)
  images = ProductImageSerializer(many=True, read_only=True)
  id = serializers.UUIDField(read_only=True)
  class Meta:
    model = Product
    fields = ['id',
              'user',
              'name',
              'description',
              'category',
              'price',
              'location',
              'stock',
              'available',
              'created',
              'updated',
              'active',
              'variations',
              'images']
    
    def create(self, validated_data):
        user = self.context.get('user')
        product = Product.objects.create(user=user,**validated_data)
        return product
    
class CategorySerializer(ModelSerializer):
  products = ProductSerializer(many=True, read_only=True)
  class Meta:
    model = Category 
    fields = ['name','description','parent','products']

class CartSerializer(ModelSerializer):
  class Meta:
    model = Cart 
    fields = ['id','user','created','updated']

class CartItemSerializer(ModelSerializer):
  product = ProductSerializer(many=True, read_only=True)
  variation = ProductVariationSerializer(many=True, read_only=True)
  class Meta:
    model = CartItem 
    fields = ['cart','product','variation','quantity']