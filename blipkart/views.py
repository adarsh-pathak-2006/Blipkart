from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from products.models import product


def home(request):
    items = product.objects.all().order_by('id')
    return render(request, 'home.html', {'item': items})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')

        if not name or not email or not password:
            messages.error(request, 'All fields are required.')
            return render(request, 'register.html')

        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'register.html')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name,
        )
        login(request, user)
        messages.success(request, 'Account created successfully.')
        return redirect('home')

    return render(request, 'register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    next_url = request.GET.get('next', '')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        posted_next = request.POST.get('next', '').strip()

        user = authenticate(request, username=email, password=password)
        if user is None:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'login.html', {'next': posted_next or next_url})

        login(request, user)
        messages.success(request, 'Logged in successfully.')
        if posted_next:
            return redirect(posted_next)
        if next_url:
            return redirect(next_url)
        return redirect('home')

    return render(request, 'login.html', {'next': next_url})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


@login_required(login_url='login')
def account(request):
    cart_ids = request.session.get('cart', [])
    items = product.objects.filter(id__in=cart_ids)
    total = sum(p.price for p in items)

    context = {
        'cart_count': len(cart_ids),
        'cart_total': total,
    }
    return render(request, 'account.html', context)
