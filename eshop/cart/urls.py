from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_detail, name="cart_detail"),
    path("add/<product_pk>/", views.cart_add, name="cart_add"),
    path("remove/<product_pk>/", views.cart_remove, name="cart_remove"),
]
