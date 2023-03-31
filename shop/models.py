from django.db import models
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    stock = models.PositiveIntegerField(blank=True)
    isbn_no = models.CharField(primary_key=True, max_length=50, db_index=True, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}, {self.pk}"

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.pk])
