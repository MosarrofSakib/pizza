from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render, redirect
from django import forms

# Create your views here
def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message":None})
    context = {
        "user":request.user
    }
    return render(request, "orders/homepage.html", context)

def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "orders/login.html", {"message":"invalid credentials!"})

def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message":"You have been successfully logged out"})

def menu(request):
    context = {
        "pizza": Pizza.objects.all()
    }
    return render(request, "orders/menu.html", context)

def add_to_cart(request):
    #gets the items from the active order
    #note that this query returns ALL the items that match the criteria
    # regular = Cart.objects.get(name = regular)
    # sicilian = Cart.objects.get(name = sicilian)

    #need some way to add only the clicked item to the cart
    ## query for the id of the clicked item, add it to cart, then query from cart?
    order = Pizza.objects.get()

    #create a new item in the cart

    #filter out the completed orders
    new_order = Order.filter(user = request.user, complete = False, )
    if new_order.exists():
        pass
    else:
        pass
