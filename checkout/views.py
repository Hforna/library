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
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.urls import reverse


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
    
    if not carts.exists():
        return redirect("/home")

    return render(request, "checkout/cart.html", context={"carts": carts, "total_price": total_price, 'quantity_options': quantity_options})

@login_required
def shipping(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        client = Client.objects.get(userr=request.user)
    except ObjectDoesNotExist:
        messages.success(request, "Complete your profile")
        return redirect("profile")
    
    try:
        shipping = Shipping.objects.filter(userr=request.user).first()
        carts = Cart.objects.filter(user=request.user)
        total_price = 0
        list_books = ""
        string_names = ""
        images = []
        for cart in carts:
            list_books += cart.book.description + ", "
            string_names += cart.book.book_name + ", "
            cart.book.price_rent *= cart.quantity
            images.append(cart.book.images)
            total_price += cart.book.price_rent

        if request.method == "GET":
            products = stripe.Product.create(
                name = string_names,
                default_price_data = {
                    "unit_amount": total_price * 100,
                    "currency": "brl",
                },
                images =  images,
                description = list_books
            )          
            products.save()
        return render(request, "checkout/shipping.html", context={"shipping": shipping, "total_price": total_price, 'products': products})
    except ObjectDoesNotExist:
        if request.method == "POST":
            address = request.POST["addressLine"]
            city = request.POST["city"]
            state = request.POST["state"]
            cep = request.POST["zipCode"]
            shipping = Shipping.objects.create(userr=request.user, address=address, cep=cep, state=state, city=city)
            return redirect("shipping")
        return render(request, "checkout/shipping_form.html")
    

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)
@csrf_exempt
def create_session(request, id):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id = request.user.id,
                success_url=domain_url + 'checkout/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'checkout/cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'quantity': 1,
                        'price': str(id),
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
        
class SuccessPayment(TemplateView):
    template_name = "checkout/success.html"

class CancelledPayment(TemplateView):
    template_name = "checkout/cancelled.html"

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session['customer_details']['email']
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=100)

        for item in line_items:
            price_product = item.amount_total / 100
        
        send_mail(message = f"""Here is your product:
        Price: {price_product}
""",
            subject = "Congratulations! You have successfully completed your purchase",
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = [customer_email],
            fail_silently=False,
)

        print(f"Payment was successful. User email: {customer_email} Price: {price_product}")

    return HttpResponse(status=200)

    
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