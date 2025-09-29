import logging
from typing import Any, Type

from django.db.models.base import Model
from django.db.models.signals import post_save
from django.dispatch import receiver

from config.settings.base import AUTH_USER_MODEL
from core_apps.profiles.models import Profile

logger = logging.getLogger(__name__)

@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(sender: Type[Model], instance: Model, created: bool, **kwargs: Any) -> None:
    """Create a profile for each new user."""
    if created:
        Profile.objects.create(user=instance)
        logger.debug(f'Profile created for user {instance.first_name} {instance.last_name}')
    else:
        logger.debug(f'Profile already exists for user {instance.first_name} {instance.last_name}')
        