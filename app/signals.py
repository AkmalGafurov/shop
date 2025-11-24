from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product, Category


print("[SIGNAL] signals.py yuklandi")

@receiver(post_save, sender=Product)
def product_saved_signal(sender, instance, created, **kwargs):
    if created:
        print(f"[SIGNAL] Yangi product yaratildi: {instance.name}")
    else:
        print(f"[SIGNAL] Product yangilandi: {instance.name}")


@receiver(post_delete, sender=Category)
def category_deleted_signal(sender, instance, **kwargs):
    print(f"[SIGNAL] Category ochirildi: {instance.title}")
