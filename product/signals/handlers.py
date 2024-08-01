from django.db.models.signals import post_save
from product.models import CustomUser, Cart
from django.dispatch import receiver
from django.utils import timezone
 
@receiver(post_save, sender=CustomUser)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)