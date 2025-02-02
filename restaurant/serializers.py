from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Menu, Booking, MenuItems, Category, User

class menuItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItems
        fields = ['title', 'price', 'inventory']

class bookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['name', 'guests', 'table', 'date']

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class MenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = MenuItems
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']
