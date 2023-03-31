from cart.forms import CartAddProductForm

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAdminUser

from .models import Product
from .serializers import ProductSerializer


# List
def product_list(request):
    products = Product.objects.all()
    search_term = ""

    paginator = Paginator(products, 20)  # Show 21 books per page.
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    if "search" in request.GET:
        search_term = request.GET["search"]
        products = Product.objects.filter(name__icontains=search_term)
        if products:
            messages.success(request, "You searched " + search_term)
        else:
            messages.success(request, "Book not found")

    query = request.GET.get("q")
    if query:
        products = Product.objects.filter(Q(name__icontains=query)).distinct()
        return render(request, "shop/product_list.html", {"products": products, "page_obj": page_obj})

    context = {"products": products, "search_term": search_term, "page_obj": page_obj}
    return render(request, "shop/product_list.html", context)


# detail
def product_detail(request, pk):
    if not request.user.is_authenticated:
        return redirect("login")
    product = get_object_or_404(Product, pk=pk)

    cart_product_form = CartAddProductForm()

    context = {
        "product": product,
        "cart_product_form": cart_product_form,
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
