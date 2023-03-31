from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "stock", "isbn_no"]
    list_filter = ["name", "price", "stock", "isbn_no"]
    save_as = True
    list_per_page = 10
