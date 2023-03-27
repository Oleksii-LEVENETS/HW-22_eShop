from cart.forms import CartAddProductForm

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Product


# List
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

    query = request.GET.get("q")
    if query:
        products = Product.objects.filter(Q(name__icontains=query)).distinct()
        return render(request, "shop/product_list.html", {"products": products})

    context = {"products": products, "search_term": search_term}
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
