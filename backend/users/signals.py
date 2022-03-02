from django.db.models.signals import pre_save
from django.contrib.auth.models import User


def update_user(sender, user, **kwargs):
    if user.email:
        user.username = user.email


pre_save.connect(update_user, sender=User)
