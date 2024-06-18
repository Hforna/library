from django.db import models
from django.contrib.auth.models import User
from library_app.models import Book

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()