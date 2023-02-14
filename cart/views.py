from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from pure.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from django.http import JsonResponse
from django.db.models import Q


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = request.POST.get('quantity')
    qty = int(quantity)
    if 'plus-cart' in request.POST:
        qty = qty + 1
    if 'minus-cart' in request.POST:
        if qty > 0:
            qty = qty - 1
            if qty == 0:
                cart.remove(product)
        else:
            print('else', qty)
            cart.remove(product)
    if qty >= 1:
        cart.add(product=product, quantity=qty)
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity']})
    return render(request, 'cart/cart_detail.html', {'cart': cart})
