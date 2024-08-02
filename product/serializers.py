from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Product, Category, ProductImage, ProductVariation, Cart, CartItem, LikedProducts

class ProductVariationSerializer(ModelSerializer):
  class Meta:
    model = ProductVariation
    fields = ['name','price','stock']

class ProductImageSerializer(ModelSerializer):
  class Meta:
    model = ProductImage
    fields = ['id','image','alt_text']

class ProductSerializer(ModelSerializer):
  variations = ProductVariationSerializer(many=True, read_only=True)
  images = ProductImageSerializer(many=True, read_only=True)
  id = serializers.UUIDField(read_only=True)
  category = serializers.SerializerMethodField()

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

  def get_category(self, obj):
    return obj.category.name if obj.category else None
    
class RecursiveCategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'children']

    def get_children(self, obj):
        children = Category.objects.filter(parent=obj)
        serializer = self.__class__(children, many=True)
        return serializer.data

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


class LikedProductsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = LikedProducts
        fields = ['id', 'product']