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
        return f"{self.name}, {self.isbn_no}"

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.pk])


class Order(models.Model):
    id = models.PositiveIntegerField(primary_key=True, db_index=True, unique=True)  # noqa: A003
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    paid = models.BooleanField()

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    id = models.PositiveIntegerField(primary_key=True, db_index=True, unique=True)  # noqa: A003
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"OrderItem {self.id}"

    def get_cost(self):
        return self.price * self.quantity
