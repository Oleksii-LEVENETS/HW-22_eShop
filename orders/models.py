from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from orders import tasks

from shop.models import Product


class Order(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"OrderItem {self.id}"

    def get_cost(self):
        return self.price * self.quantity


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


@receiver(post_delete, sender=Order)
def back_order_to_shop(sender, instance, **kwargs):
    orderitems = OrderItem.objects.filter(order=instance.pk)
    for orderitem in orderitems:
        product = Product.objects.get(pk=orderitem.product.pk)
        product.stock = product.stock + orderitem.quantity
        product.save()
