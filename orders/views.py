from api import api_order_new, api_orderitem

from cart.cart import Cart

from django.shortcuts import render

from orders import tasks

from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAdminUser

from .forms import OrderCreateForm
from .models import Order, OrderItem
from .serializers import OrderItemSerializer, OrderSerializer


def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            api_order_new(
                pk=order.pk,
                first_name=order.first_name,
                last_name=order.last_name,
                email=order.email,
                phone_number=order.phone_number,
                city=order.city,
                created=order.created,
                updated=order.updated,
                paid=order.paid,
            )
            for item in cart:
                orderitem = OrderItem.objects.create(
                    order=order, product=item["product"], price=item["price"], quantity=item["quantity"]
                )
                api_orderitem(
                    pk=orderitem.pk,
                    order=orderitem.order.pk,
                    product=orderitem.product.pk,
                    price=orderitem.price,
                    quantity=orderitem.quantity,
                )
            cart.clear()

            orderitems = OrderItem.objects.filter(order_id=order.id)
            dict_orderitems = {}
            for num, item in enumerate(orderitems):
                dict_item = {
                    "product.name": item.product.name,
                    "product.isbn_no": item.product.isbn_no,
                    "price": item.product.price,
                    "quantity": item.quantity,
                    "get_cost": item.get_cost(),
                }
                dict_orderitems[num + 1] = dict_item
            subject = f"New Order {order.pk} created {order.created}."
            message = f"""
                First name: {order.first_name}
                Last name: {order.last_name}
                Phone number: {order.phone_number}
                City: {order.city}
                Created: {order.created}
                Order items: {dict_orderitems}
                Order Total Cost: {order.get_total_cost()}
            """
            user_email = order.email
            tasks.send_mail_temp.delay(subject, message, user_email)

            return render(request, "orders/order_created.html", {"order": order})
    else:
        form = OrderCreateForm(
            initial={
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "email": request.user.email,
            }
        )

    return render(request, "orders/order_create.html", {"cart": cart, "form": form})


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    permission_classes = (IsAdminUser,)
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def perform_create(self, serializer):
        serializer.save()


class OrderViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    permission_classes = (IsAdminUser,)
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def perform_create(self, serializer):
        serializer.save()
