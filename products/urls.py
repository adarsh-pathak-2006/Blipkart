from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
]
