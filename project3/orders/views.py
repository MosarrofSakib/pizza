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
from django.db.models import F, Avg, Count, Min, Sum
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import stripe
import json
import secrets
import string
import random
from random import randint

# Create your views here


def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})
    context = {
        "user": request.user
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
        return render(request, "orders/login.html", {"message": "invalid credentials!"})


def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Thanks for coming!"})


def menu(request):
    context = {
        "pizza": Pizza.objects.all(),
        "cart": Cart.objects.filter(user=request.user),
        "sicilian": Sicilian.objects.all()
    }

    # if there is no active order
    if Order.objects.filter(user=request.user, complete=False).exists() == False:
        context = {
            "pizza": Pizza.objects.all(),
            "cart": Cart.objects.filter(user=request.user),
            "sicilian": Sicilian.objects.all()
        }
    else:
        context = {
            "pizza": Pizza.objects.all(),
            "cart": Cart.objects.filter(user=request.user),
            "sicilian": Sicilian.objects.all(),
            "active": Order.objects.get(user=request.user, complete=False)
        }
    return render(request, "orders/menu.html", context)


@login_required(login_url='/orders/login/')
def add_to_cart(request, item_id):

    # query database for the correct item
    # the filter queryset is returning ALL items that match this query
    order = Pizza.objects.get(id=item_id)

    # consider using get to return a single object to manipulate for the final price

    # generate a new active order if one does not already exist
    if Order.objects.filter(user=request.user, complete=False).exists() == False:
        Order.objects.create(user=request.user, complete=False, subtotal=0)

    # get user's current order
    current = Order.objects.get(user=request.user, complete=False)

    # get the total price of the items in the cart
    # total = Cart.objects.filter(user = request.user).aggregate(Sum('price'))['price__sum'] #returns the value of the price__sum key

    # if item already exists in cart, increase it's quantity by one and add the price to the subtotal
    if Cart.objects.filter(user=request.user, pizza=order.item).exists():
        Cart.objects.filter(user=request.user, pizza=order.item,
                            price=order.price).update(quantity=F('quantity') + 1)
        Order.objects.filter(user=request.user, complete=False).update(
            subtotal=current.subtotal + order.price)

    # if item does not exist, add it to the Cart and update the price
    else:
        new_item = Cart.objects.create(
            user=request.user, id=item_id, pizza=order.item, price=order.price)
        Order.objects.filter(user=request.user).update(
            subtotal=current.subtotal + order.price)

    # reverse the user back to the menu
    return HttpResponseRedirect(reverse("menu"))


@login_required(login_url='/orders/login/')
def remove_from_cart(request, cart_id):
    # query for the object in the cart and the current subtotal
    item = Cart.objects.get(user=request.user, id=cart_id)
    current = Order.objects.get(user=request.user, complete=False)

    # remove the clicked object from the database
    item.delete()

    # get all the items currently in the cart
    #cart = Cart.objects.filter(user = request.user)

    # reduce the subtotal of the order
    #Order.objects.filter(user = request.user, complete = False).update(subtotal = current.price - item.price)

    # try calculating the new subtotal using the aggregate method instead of adding/subtracting
    #Order.objects.filter(user = request.user, complete = False).update(subtotal = cart.aggregate(Sum('price')))
    if Cart.objects.filter(user=request.user).count() == 0:
        total = 0.00
    else:
        total = Cart.objects.filter(user=request.user).aggregate(Sum('price'))[
            'price__sum']  # returns the value of the price__sum key

    Order.objects.filter(
        user=request.user, complete=False).update(subtotal=total)

    return HttpResponseRedirect(reverse("menu"))

# complete the order


@login_required(login_url='/orders/login/')
def place_order(request):
    if Order.objects.filter(user=request.user, complete=False).exists():
        Order.objects.filter(
            user=request.user, complete=False).update(complete=True)
    else:
        pass
        # notify the user that there are no items currently in the cart
    Cart.objects.filter(user=request.user).delete()
    return HttpResponseRedirect(reverse('menu'))


@login_required(login_url='/orders/login/')
def checkout(request):
    stripe.api_key = settings.STRIPE_PUBLISHABLE_KEY
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'price': Order.objects.get(user=request.user, complete=False).subtotal,
                'product_data': {
                    'name': 'order',
                },
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('menu')) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('index'))
    )
    context = {
        'session_id': session.id,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY
    }
    return render(request, 'orders/orders.html', context)


# #configurate the stripe api and payments
# @csrf_exempt
# def stripe_config(request):
#     if request.method == 'GET':
#         stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
#         return JsonResponse(stripe_config, safe=False)


# place order and charge the customer using the Stripe API
# @login_required(login_url = '/orders/login/')
# def checkout(request):
#
#     @csrf_exempt
#     def createpayment(request):
#         if request.user.is_authenticated:
#             total = Orders.objects.filter(user = request.user, complete = False).subtotal
#             stripe.api_key = 'sk_test_51HGRDpI2Nu98lgt7LnizEKT7bPmeABSwfX4HQTm1NK1BtaHora6uGrgQfeQae17vI92aIterXKiA0PD4OVtZwyBB008wEHd2hT'
#             if request.method == 'POST':
#                 data = json.loads(request.body)
#                 intent = stripe.PaymentIntent.create(amount=total, currency=data['currency'], metadata={'integration_check': 'accept_a_payment'})
#                 try:
#                     return JsonResponse({'publishableKey':'pk_test_51HGRDpI2Nu98lgt7CcGeNFQRZiqjTMM9emJ28YerE7zUVHhQTXszGMZAEGptEYHQSMRnStGzMo0C9L8ZXr1JBDrz00evkTwDCU', 'clientSecret': intent.client_secret})
# 			except Exception as e:
# 				return JsonResponse({'error':str(e)},status= 403)

# @csrf_exempt
# def create_checkout_session(request):
#     if request.method == 'GET':
#         domain_url = 'http://localhost:8000/menu'
#         stripe.api_key = settings.STRIPE_SECRET_KEY
#         try:
#             # Create new Checkout Session for the order
#             # Other optional params include:
#             # [billing_address_collection] - to display billing address details on the page
#             # [customer] - if you have an existing Stripe Customer ID
#             # [payment_intent_data] - lets capture the payment later
#             # [customer_email] - lets you prefill the email input in the form
#             # For full details see https:#stripe.com/docs/api/checkout/sessions/create
#
#             # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
#             checkout_session = stripe.checkout.Session.create(
#                 success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
#                 cancel_url=domain_url + 'cancelled/',
#                 payment_method_types=['card'],
#                 mode='payment',
#                 line_items=[
#                     {
#                         'name': 'T-shirt',
#                         'quantity': 1,
#                         'currency': 'usd',
#                         'amount': '2000',
#                     }
#                 ]
#             )
#             return JsonResponse({'sessionId': checkout_session['id']})
#         except Exception as e:
#             return JsonResponse({'error': str(e)})
