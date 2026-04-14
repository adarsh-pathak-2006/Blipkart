from django.shortcuts import render,redirect
from products.models import product


def home(request):
    item=product.objects.all()
    return render(request, 'home.html',{ 'item':item  })

def cart(request):
    return render(request, 'cart.html')

def account(request):
    return render(request, 'account.html')


def add_cart(request,id):
    cart=request.session.get('cart',[])
    if id not in cart:
        cart.append(id)  
    request.session['cart']=cart
    return redirect('home')