from django.http import HttpResponse
from django.shortcuts import render
# from .models import Menu

# Create your views here.
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