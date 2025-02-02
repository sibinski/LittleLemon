from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpResponse
from rest_framework import request, generics
import rest_framework
import rest_framework.generics
from rest_framework.response import Response
from rest_framework import decorators
from restaurant.serializers import bookingSerializer, menuItemsSerializer, userSerializer
from .models import Booking, Menu, MenuItems
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .serializers import MenuItemSerializer, menuItemsSerializer


# Create your views here.
class bookingView(APIView):
    def get(self, request):
        permission_classes=[IsAuthenticated]
        items = Booking.objects.all()
        serializer = bookingSerializer(items, many=True)
        return Response(serializer.data) # Return JSON

    def post(self, request):
        permission_classes=[IsAuthenticated]
        serializer = menuItemsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"success", "data": serializer.data})


#@api_view(["GET", "POST"])
#@permission_classes([IsAuthenticated])
#class UserViewSet(ModelViewSet):
#    def get(self, request):
#        queryset = User.objects.all()
#        serializer = userSerializer(QuerySet, many=True)
#        return Response(serializer.data)
#
#    def post(self, request):
#        queryset = User.objects.all()
#        serializer = userSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response({"status":"success", "data": serializer.data})


class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItems.objects.all()
    serializer_class = menuItemsSerializer
    permission_classes = [IsAuthenticated]
    api_view = ["GET", "POST"]
    

class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItems.objects.all()
    serializer_class = menuItemsSerializer
    api_view = ["GET","PUT", "DELETE"]


def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data}) 

def sayHello(request):
    return HttpResponse('Hello World!')

def index(request):
    return render(request, 'index.html', {})
def home(request):
    return render(request, 'index.html', {})
def about(request):
    return render(request, 'index.html', {})
def book(request):
    return render(request, 'index.html', {})
def display_menu_items(request):
    return render(request, 'index.html', {})