from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

def generate_random_code():
  return str(uuid.uuid4())[:5]

class CustomUser(AbstractUser):
  id = models.CharField(primary_key=True,max_length=6,default=generate_random_code)
  email = models.EmailField(unique=True)
  is_active = models.BooleanField(default=False)
  
  def __str__(self):
    return self.username
  
class UserProfile(models.Model):
  user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
  profile_image = models.Image