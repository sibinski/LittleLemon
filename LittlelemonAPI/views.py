import re
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.decorators import api_view, action, permission_classes, throttle_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics
from rest_framework import viewsets
from .models import MenuItems, Cart, OrderItem, Order, Category, OrderItem
from .serializers import MenuItemSerializer, CategorySerializer, OrderSerializer, CartSerializer
from LittlelemonAPI import serializers
from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import UserRateThrottle
from django.contrib.auth.models import User, Group
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Create your views here.
class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItems.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price']
    filterset_fields = ['price']
    search_fields = ['title']

class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
        queryset = MenuItems.objects.all()
        serializer_class = MenuItemSerializer

class MenuItemsViewSet(viewsets.ModelViewSet):
    queryset = MenuItems.objects.all()
    serializer_class = MenuItemSerializer

@api_view(['GET', 'POST', 'PATCH'])
@permission_classes([IsAuthenticated])
def single_item(request, id):
    item = get_object_or_404(MenuItems, pk=id)
    if request.method=='GET':
        serialized_item = MenuItemSerializer(item) 
        return Response(serialized_item.data)
    if request.method == 'PATCH':
        if request.user.groups.filter(name='Manager').exists:
            serialized_item = MenuItemSerializer(item, data=request.data, partial=True)
            if serialized_item.is_valid():
                serialized_item.save()
                return Response(serialized_item.data)
            return Response(serialized_item.errors, status=400)
        else:
            raise PermissionDenied("You don't have permission to patch this item.")


@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message":"Some secret message"})

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"message":"only Manager should see this!"})
    else:
        return Response({"message":"You are not authorized"}, 403)

@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message":"successfull"})

@api_view()
@throttle_classes([UserRateThrottle])
def throttle_check_auth(request):
    return Response({"message":"successfull"})

@api_view(['POST', 'DELETE', 'GET'])
@permission_classes([IsAdminUser])
def managers(request):
    if(request.method=='GET'):
        managers = Group.objects.get(name="Manager")
        managers_list = managers.user_set.all().values("id", "username", "email")
        return Response({"list of managers":list(managers_list)})
    username = request.data['username']
    if (username):
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Manager")
        if(request.method=='POST'):
            managers.user_set.add(user)
        elif(request.method=='DELETE'):
            managers.user_set.remove(user)
            return Response({"message":"ok"})
        else:
            return Response({"message":"error"}, status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'DELETE'])
@permission_classes([IsAdminUser])
def delivery_crew(request):
    username = request.data['username']
    if (username):
        user = get_object_or_404(User, username=username)
        delivery_crew_members = Group.objects.get(name="Delivery_Crew")
        if(request.method=='POST'):
            delivery_crew_members.user_set.add(user)
        elif(request.method=='DELETE'):
            delivery_crew_members.user_set.remove(user)
        return Response({"message":"ok"})
    else:
        return Response({"message":"error"}, status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'DELETE'])
@permission_classes([IsAdminUser])
def manage_delivery_orders(request):
    if request.method == 'POST':
        user_username = request.data.get('user')
        delivery_crew_username = request.data.get('delivery_crew')
        if not(user_username and delivery_crew_username):
            return Response({"message" : "user and delivery crew username are required"}, status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, username=user_username) 
        order = get_object_or_404(Order, user=user )
        delivery_crew_member = get_object_or_404(User, username = delivery_crew_username)
        if not delivery_crew_member.groups.filter(name='delivery_crew').exists():
            return Response({"message":"User is not a delivery crew member!"}, status.HTTP_400_BAD_REQUEST)
        order.assigned_to = delivery_crew_member
        order.save()
        return Response({"message":"Order assigned successfully!"}, status.HTTP_200_OK)
    elif request.method == 'DELETE':
        order = request.data.get('order')
        order = get_object_or_404(Order)
        order.assigned_to = None
        order.save()
        return Response({"message":"Order unassigned successfully!"}, status.HTTP_200_OK)

class DeliveryCrewViewSet(viewsets.ViewSet):

    def create(self, request):
        #only for super admin and managers
        if self.request.user.is_superuser == False:
            if self.request.user.groups.filter(name='Manager').exists() == False:
                return Response({"message":"forbidden"}, status.HTTP_403_FORBIDDEN)
        
        user = get_object_or_404(User, username=request.data['username'])
        dc = Group.objects.get(name="Delivery_Crew")
        dc.user_set.add(user)
        return Response({"message": "user added to the delivery crew group"}, 200)

    def destroy(self, request):
        #only for super admin and managers
        if self.request.user.is_superuser == False:
            if self.request.user.groups.filter(name='Manager').exists() == False:
                return Response({"message":"forbidden"}, status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, username=request.data['username'])
        dc = Group.objects.get(name="Delivery_Crew")
        dc.user_set.remove(user)
        return Response({"message": "user removed from the delivery crew group"}, 200)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def cart_items(request):
    if request.method == 'GET':
        cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = CartSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':
        item_id = request.data.get('item_id')
        cart_item = get_object_or_404(Cart, id=item_id, user = request.user)
        serializer = CartSerializer(cart_item, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        item_id = request.data.get('item_id')
        cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
        queryset = cart_item.filter('item_id')
        cart_item.delete()
        return Response({"message":"cart item removed"}, status=HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def customer_orders(request):
    if request.method == 'GET':
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save(user=request.user)  # Attach the logged-in user to the order
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view()
@permission_classes([IsAuthenticated])
def me(request):
    return Response(request.user.email)