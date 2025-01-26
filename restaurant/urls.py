from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('', views.index, name="index"),
    path('restaurant/', views.sayHello, name="sayHello"),
    path('about/', views.about, name="about"),
    path('book/',views.book, name="book"),
    path('menu/', views.menu, name="menu"),
    path('menu_items/<int:pk>/', views.display_menu_items, name="menu_items"),
    ]