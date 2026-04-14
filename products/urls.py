from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.cart, name='cart'),
    path('remove-from-cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
]

