from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .models import product


def cart(request):
    cart_ids = request.session.get('cart', [])
    items = product.objects.filter(id__in=cart_ids)
    total = sum(p.price for p in items)

    return render(
        request,
        'cart.html',
        {
            'item': items,
            'total': total,
            'item_count': len(cart_ids),
        },
    )


def add_to_cart(request, id):
    get_object_or_404(product, id=id)

    cart_ids = request.session.get('cart', [])
    if id not in cart_ids:
        cart_ids.append(id)
        messages.success(request, 'Product added to cart.')
    else:
        messages.info(request, 'Product is already in your cart.')

    request.session['cart'] = cart_ids
    return redirect('home')


def remove_from_cart(request, id):
    cart_ids = request.session.get('cart', [])

    if id in cart_ids:
        cart_ids.remove(id)
        messages.success(request, 'Product removed from cart.')

    request.session['cart'] = cart_ids
    return redirect('products:cart')
