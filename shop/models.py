from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from rest_framework.authtoken.models import Token


class Product(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    stock = models.PositiveIntegerField(blank=True)
    isbn_no = models.CharField(primary_key=True, max_length=50, db_index=True, default="isbn_no", unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.pk])


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created and instance.is_superuser:
#         Token.objects.create(user=instance)
