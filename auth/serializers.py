from rest_framework import serializers
from .models import CustomUser, UserProfile

class UserCreateSerializer(serializers.ModelSerializer):
  id = serializers.CharField(read_only=True)
  class Meta:
    model = CustomUser
    fields = ['id','username','email','password']

  def create(self, validated_data):
    return CustomUser.objects.create_user(**validated_data)
  
class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserProfile
    fields = ['user','bio','profile_picture','date_of_birth']