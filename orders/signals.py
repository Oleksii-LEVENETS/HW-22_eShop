from .models import Order, OrderItem
from .tasks import send_mail_temp

from django.contrib.sites.shortcuts import get_current_site
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


print("signals.py starts!")


# @receiver(post_save, sender=Order)
# def create_order(sender, instance, created, **kwargs):
#     orderitems = list(OrderItem.objects.filter(order_id=instance.id))
#     if created:
#         subject = f"New Order {instance.pk} created {instance.created}."
#         message = f"First name: {instance.first_name}" \
#                   f"Last name: {instance.last_name}" \
#                   f"Phone number: {instance.phone_number}" \
#                   f"City: {instance.city}" \
#                   f"Created: {instance.created}" \
#                   f"Order items: {orderitems}"
#
#         user_email = instance.email
#         send_mail_temp.delay(subject, message, user_email)
