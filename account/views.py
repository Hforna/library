from django.shortcuts import render, redirect
from .models import Client
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def account(request):
    try:
        client = Client.objects.get(userr=request.user)
        if request.method == "POST":
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

        return render(request, "account/account.html", context={"client": client})
    except ObjectDoesNotExist:
        if request.method == "POST":
            full_name = request.POST["full_name"]
            phone = request.POST["phone"]
            birthday = request.POST["birthday"]
            country = request.POST["country"]
            client = Client.objects.create(userr=request.user, full_name=full_name, phone=phone, birthday=birthday, country=country)
            client.save()
            return redirect("account")
        return render(request, "account/account.html")

