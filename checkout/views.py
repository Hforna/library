from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView
from library_app.models import Book, Author
from .models import Cart
from account.models import Client, Shipping
from django.core.mail import send_mail
from rolepermissions.roles import assign_role, get_user_roles
from rolepermissions.decorators import has_role_decorator
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.http import HttpResponse
from library_project import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def cart(request):
    carts = Cart.objects.filter(user=request.user)
    quantity_options = range(1, 21)
    total_price = 0
    for cart in carts:
        cart.book.price_rent *= cart.quantity
        total_price += cart.book.price_rent


    if request.method == "POST":
        quantity = request.POST["quantity"]
        carts_id = request.POST.get("cart_id")
        cart = Cart.objects.get(id=carts_id)
        cart.quantity = quantity
        cart.save()
        return redirect("cart")

    return render(request, "checkout/cart.html", context={"carts": carts, "total_price": total_price, 'quantity_options': quantity_options})

@login_required
def shipping(request):
    try:
        client = Client.objects.get(userr=request.user)
    except ObjectDoesNotExist:
        messages.success(request, "Complete your profile")
        return redirect("profile")
    
    try:
        shipping = Shipping.objects.get(userr=request.user)
        carts = Cart.objects.filter(user=request.user)
        total_price = 0
        for cart in carts:
            cart.book.price_rent *= cart.quantity
            total_price += cart.book.price_rent
        return render(request, "checkout/shipping.html", context={"shipping": shipping, "total_price": total_price})
    except ObjectDoesNotExist:
        if request.method == "POST":
            address = request.POST["addressLine"]
            city = request.POST["city"]
            state = request.POST["state"]
            cep = request.POST["zipCode"]
            shipping = Shipping.objects.create(userr=request.user, address=address, cep=cep, state=state, city=city)
            return redirect("shipping")
        return render(request, "checkout/shipping_form.html")
    
@login_required
def payment(request):
    return render(request, "checkout/payment.html")

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)
@csrf_exempt
def create_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create
            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'quantity': 1,
                        'price': "price_1PXlUF01ThTiNs0ZxH2XqjGE",
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    
@login_required
def edit_shipping(request):
    shipping = Shipping.objects.get(userr=request.user)
    if request.method == "POST":
        address = request.POST["address"]
        city = request.POST["city"]
        state = request.POST["state"]
        cep = request.POST["zipCode"]
        shipping.address = address
        shipping.city = city
        shipping.state = state
        shipping.cep = cep
        shipping.save()
        return redirect("shipping")
    
    return render(request, "checkout/edit_shipping.html", context={"shipping": shipping})
    
@login_required
def delete_item_cart(request, pk):
    cart = Cart.objects.get(pk=pk)
    cart.delete()
    return redirect("/checkout/cart")