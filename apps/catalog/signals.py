from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Product, Category

@receiver([post_save, post_delete], sender=Product)
@receiver([post_save, post_delete], sender=Category)
def clear_catalog_cache(sender, **kwargs):
    cache.clear()
