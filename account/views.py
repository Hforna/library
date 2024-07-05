from django.shortcuts import render, redirect
from .models import Client, Shipping
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib import messages

# Create your views here.

def account(request):
    try:
        shipping = Shipping.objects.get(userr=request.user.id)
        if "update_shipping" in request.POST:
            address = request.POST["shipping_address"]
            city = request.POST["city"]
            state = request.POST["state"]
            cep = request.POST["zip_code"]
            shipping.address = address
            shipping.city = city
            shipping.state = state
            shipping.cep = cep
            shipping.save()
            messages.success(request, "Shipping information updated")
            return redirect("account")
    except ObjectDoesNotExist:
        if request.method == "POST":
            address = request.POST["shipping_address"]
            city = request.POST["city"]
            state = request.POST["state"]
            cep = request.POST["zip_code"]
            shipping = Shipping.objects.create(userr=request.user, address=address, city=city, state=state, cep=cep)
            shipping.save()
            messages.success(request, "Shipping information updated")
            return redirect("account")



    try:
        client = Client.objects.get(userr=request.user)
        if "update_account" in request.POST:
            full_name = request.POST["full_name"]
            phone = request.POST["phone"]
            birthday = request.POST["birthday"]
            country = request.POST["country"]
            client.full_name = full_name
            client.phone = phone
            client.birthday = birthday
            client.country = country
            client.save()
            return redirect("account")
    except ObjectDoesNotExist:
        if request.method == "POST":
            full_name = request.POST["full_name"]
            phone = request.POST["phone"]
            birthday = request.POST["birthday"]
            country = request.POST["country"]
            client = Client.objects.create(userr=request.user, full_name=full_name, phone=phone, birthday=birthday, country=country)
            client.save()
            messages.success(request, "Account information updated")
            return redirect("account")
    except ValidationError:
        messages.error(request, "The data is invalid")
        return redirect("account")
        

    return render(request, "account/account.html", context={"client": client, "shipping": shipping})

