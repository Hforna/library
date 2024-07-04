from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    userr = models.OneToOneField(User, on_delete=models.CASCADE, default="")
    full_name = models.CharField(max_length=256)
    phone = models.CharField(max_length=11)
    birthday = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.full_name} your phone is {self.phone}"

class Shipping(models.Model):
    userr = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    cep = models.CharField(max_length=12, default="")
    city = models.CharField(max_length=60, default="")
    address = models.CharField(max_length=256, default="")
    state = models.CharField(max_length=256, default="")


