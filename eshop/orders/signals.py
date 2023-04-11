from api import api_cart, api_order_delete, api_orderitem_delete

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from orders import tasks
from orders.models import Order, OrderItem

from shop.models import Product


@receiver(post_save, sender=Order)
def change_order_to_done(sender, instance, update_fields, **kwargs):
    if update_fields:
        subject = f"Order {instance.id} is done."
        message = f"""
        Please, wait for the delivery you order {instance.id}.
        We just sent it.

        Your BookShop Team.
        """
        user_email = instance.email
        tasks.send_mail_temp.delay(subject, message, user_email)


@receiver(post_delete, sender=OrderItem)
def back_orderitem_to_shop(sender, instance, **kwargs):
    product = Product.objects.get(pk=instance.product.pk)
    product.stock = product.stock + instance.quantity
    product.save()
    api_cart(pk=instance.product.pk, stock=product.stock)
    api_orderitem_delete(instance.pk)


@receiver(post_delete, sender=Order)
def back_order_to_shop(sender, instance, **kwargs):
    orderitems = OrderItem.objects.filter(order=instance.pk)
    for orderitem in orderitems:
        product = Product.objects.get(pk=orderitem.product.pk)
        product.stock = product.stock + orderitem.quantity
        product.save()
        api_cart(pk=orderitem.product.pk, stock=product.stock)
    api_order_delete(instance.pk)
