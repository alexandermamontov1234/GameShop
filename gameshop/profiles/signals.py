from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# @receiver(post_save, sender=CustomerSettings)
# def update_customer_settings(sender, instance, created, **kwargs):
#     if created:
#         CustomerSettings.objects.create(user=instance)
#     instance.customersettings.save()