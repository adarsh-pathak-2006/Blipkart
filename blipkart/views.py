from django.shortcuts import render
from products.models import product


def home(request):
    item=product.objects.all()
    return render(request, 'home.html',{ 'item':item  })

def cart(request):
    return render(request, 'cart.html')

def account(request):
    return render(request, 'account.html')
