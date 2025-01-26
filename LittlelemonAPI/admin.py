from tkinter import Menu
from django.contrib import admin
from .models import Cart, MenuItems, Category, Order, OrderItem
admin.site.register(MenuItems)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)

