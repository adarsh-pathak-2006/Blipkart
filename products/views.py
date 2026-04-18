from smtplib import SMTPAuthenticationError, SMTPException

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import product


def cart(request):
    cart_ids = request.session.get('cart', [])
    items = product.objects.filter(id__in=cart_ids)
    total = sum(p.price for p in items)
    valid_item_ids = {p.id for p in items}
    item_count = len([pid for pid in cart_ids if pid in valid_item_ids])

    if item_count != len(cart_ids):
        request.session['cart'] = [pid for pid in cart_ids if pid in valid_item_ids]

    return render(
        request,
        'cart.html',
        {
            'item': items,
            'total': total,
            'item_count': item_count,
        },
    )


@require_POST
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


@require_POST
def remove_from_cart(request, id):
    cart_ids = request.session.get('cart', [])

    if id in cart_ids:
        cart_ids.remove(id)
        messages.success(request, 'Product removed from cart.')

    request.session['cart'] = cart_ids
    return redirect('products:cart')


@login_required(login_url='login')
@require_POST
def place_order(request):
    cart_ids = request.session.get('cart', [])
    items = product.objects.filter(id__in=cart_ids)

    if not items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('products:cart')

    total = sum(p.price for p in items)
    item_lines = '\n'.join([f'- {p.name} (Rs. {p.price})' for p in items])
    customer_name = request.user.first_name or request.user.username
    customer_email = request.user.email or request.user.username

    subject = 'New Order Received - Blipkart'
    message = (
        f'Order placed by: {customer_name} ({customer_email})\n\n'
        f'Items:\n{item_lines}\n\n'
        f'Total: Rs. {total}'
    )

    recipient = getattr(settings, 'ORDER_NOTIFICATION_EMAIL', '') or customer_email
    if not recipient:
        messages.error(request, 'Order notification email is not configured.')
        return redirect('products:cart')

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            fail_silently=False,
        )
    except SMTPAuthenticationError:
        messages.error(
            request,
            'Email authentication failed. Update EMAIL_HOST_USER/EMAIL_HOST_PASSWORD in env.txt and use a Gmail App Password.',
        )
        return redirect('products:cart')
    except (SMTPException, OSError):
        messages.error(
            request,
            'Unable to send order email right now. Please verify SMTP settings and try again.',
        )
        return redirect('products:cart')

    request.session['cart'] = []
    messages.success(request, 'Order placed successfully. Confirmation email sent.')
    return redirect('products:cart')
