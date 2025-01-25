from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Product, Cart, CartItem, User

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)


