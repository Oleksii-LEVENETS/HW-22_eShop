from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.tasks import send_mail_temp

from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created and instance.is_superuser:
        Token.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user(sender, instance, created, **kwargs):
    if created:
        subject = f"User '{instance}' is created."
        message = f"User '{instance}' is created. Is Admin: {instance.is_superuser}. Is Staff: {instance.is_staff}."
        user_email = instance.email
        send_mail_temp.delay(subject, message, user_email)
