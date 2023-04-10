from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

app_name = "shop"


urlpatterns = [
    path("", cache_page(10)(views.product_list), name="product_list"),  # ToDo: cached!
    path("product-detail/<pk>/", views.product_detail, name="product_detail"),
    path("contact/", views.contact, name="contact"),
]
