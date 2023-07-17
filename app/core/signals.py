"""
this file contains the necessary singals for the database
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """create a profile of user using django signal post_save """
    try:
        profile = UserProfile.objects.get(user=instance)
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)
    else:
        profile.save()


# post_save.connect(create_profile, sender=User)
