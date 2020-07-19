from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render, redirect
from django import forms
from .forms import RegisterForm

#still need to build a way to handle error messages
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('orders/homepage.html')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {"form":form})
