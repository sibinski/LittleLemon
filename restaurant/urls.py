from django.urls import path, include
from django.contrib import admin
from . import views
from .views import bookingView
# from .views import UserViewSet
from rest_framework.routers import BaseRouter, DefaultRouter


urlpatterns = [
  #  path('users/', UserViewSet.as_view()),
  #  path('api/', include(DefaultRouter.urls)),
  #  path('admin/', admin.site.urls),
  # path('api/', include('restaurant.urls')),
    path('', views.home, name="home"),
    path('', views.index, name="index"),
    path('restaurant/', views.sayHello, name="sayHello"),
    path('about/', views.about, name="about"),
    path('booking/',bookingView.as_view(), name="booking"),
   #path('menu/', views.menu, name="menu"),
    path('menu-item/', views.MenuItemView.as_view()),
    path('menu-item/<int:pk>/', views.SingleMenuItemView.as_view, name="single-items"),
    
    ]