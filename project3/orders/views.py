from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.decorators import login_required
from django.db.models import F

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

def show_cart(request):
    context = {
    "cart":Cart.objects.all()
    }

#@login_required(login_url = '/login/')
def add_to_cart(request, item_id):
    #query database for the correct item
    order = Pizza.objects.get(id = item_id)

    #if item already exists in cart, increase it's quantity by one
    if Cart.objects.filter(pizza = order.item).exists():
        Cart.objects.filter(pizza = order.item).update(quantity = F('quantity') + 1)
        #return render(request, "orders/index.html", {"message":order.quantity})

    #if item does not exist, add it to the Cart
    else:
        new_item = Cart.objects.create(id = item_id, pizza = order.item)

    #test connection
    return render(request, "orders/index.html", {"message":order.item})

def remove_from_cart(request, cart_id):
    context = {
    "cart": Cart.objects.all()
    }



    #return render(request, "orders/cart.html", context)

def place_order(request):
    pass
