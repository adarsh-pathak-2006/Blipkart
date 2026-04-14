from django.shortcuts import render
from products.models import product



def cart(request):
    cart = request.session.get('cart', [])
    item = product.objects.filter(id__in=cart)

    total = 0
    for p in item:
        total += p.price

    return render(request, 'cart.html', {'item': item, 'total' : total })

from django.shortcuts import redirect

def remove_from_cart(request, id):
    cart = request.session.get('cart', [])

    if id in cart:
        cart.remove(id)

    request.session['cart'] = cart

    return redirect('cart')