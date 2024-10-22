from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


def generate_random_id():
  return str(uuid.uuid4())[:5]


class CustomUser(AbstractUser):
  id = models.CharField(primary_key=True,max_length=6,default=generate_random_id)
  email = models.EmailField(unique=True)
  
  def __str__(self):
    return self.username
  
class UserStatus(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('online', 'Online'), ('offline', 'Offline')])
    last_seen = models.DateTimeField()

    class Meta:
        verbose_name_plural = "User status "

class UserProfile(models.Model):
   user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
   bio = models.TextField(null=True,blank=True)
   profile_picture = models.ImageField(upload_to='profile_picture',null=True,blank=True)
   date_of_birth= models.DateField(blank=True,null=True)

   def __str__(self) -> str:
      return f'Profile of {self.user.username}'