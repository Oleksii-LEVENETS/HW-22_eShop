from cart.cart import Cart
from cart.forms import CartAddProductForm

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page

from orders import tasks

from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAdminUser

from .forms import ContactForm
from .models import Product
from .serializers import ProductSerializer


# List
@cache_page(10 * 1)  # Cache time to live is 10 seconds
def product_list(request):
    products = Product.objects.all()
    search_term = ""

    if "search" in request.GET:
        search_term = request.GET["search"]
        products = Product.objects.filter(name__icontains=search_term)
        if products:
            messages.success(request, "You searched " + search_term)
        else:
            messages.success(request, "Book not found")

    paginator = Paginator(products, 20)  # Show 20 books per page.
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    query = request.GET.get("q")
    if query:
        products = Product.objects.filter(Q(name__icontains=query)).distinct()
        return render(request, "shop/product_list.html", {"products": products, "page_obj": page_obj})

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    cart = Cart(request)
    context = {
        "products": products,
        "search_term": search_term,
        "page_obj": page_obj,
        "num_visits": num_visits,
        "cart": cart,
    }
    return render(request, "shop/product_list.html", context)


# detail
def product_detail(request, pk):
    if not request.user.is_authenticated:
        return redirect("login")
    product = get_object_or_404(Product, pk=pk)
    cart_product_form = CartAddProductForm()
    cart = Cart(request)
    context = {
        "product": product,
        "cart_product_form": cart_product_form,
        "cart": cart,
    }

    return render(request, "shop/product_detail.html", context)


class ProductViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    permission_classes = (IsAdminUser,)
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def perform_create(self, serializer):
        serializer.save()


# Contact Us
def email_contact_form(request, form, template_name):
    data = dict()
    if request.method == "POST":
        if form.is_valid():
            subject = "Website Inquiry."
            body = {
                "first_name": form.cleaned_data["first_name"],
                "last_name": form.cleaned_data["last_name"],
                "email": form.cleaned_data["email_address"],
                "message": form.cleaned_data["message"],
            }
            message = "\n".join(body.values())
            tasks.send_mail_temp.delay(subject, message)
            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False
    context = {"form": form}
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
    else:
        form = ContactForm(initial={"first_name": "User", "last_name": "Usenko", "email_address": "uu@example.com"})
        # form = ContactForm()
    return email_contact_form(request, form, "shop/partial_contact_form_create.html")
