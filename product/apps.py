from django.apps import AppConfig


class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'product'

    def ready(self):
        from .signals.handlers import  create_cart
        from .models import CustomUser
        from django.db.models.signals import post_save
        post_save.connect(create_cart, sender=CustomUser)