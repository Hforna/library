from django.db import models
from django.contrib.auth.models import User
from account.models import Client
import time
class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    full_name = models.CharField(max_length=256)
    birthday = models.DateField(default="2024-12-12")
    country = models.CharField(max_length=256)



class Book(models.Model):
    book_name = models.CharField(max_length=256)
    is_published = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=60, default="")
    price_rent = models.IntegerField()
    description = models.CharField(max_length=600, default="")
    images = models.ImageField(default="", blank=True, null=True)
    number_visit_page = models.IntegerField(default=0)

class AvaliationsBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.CharField(max_length=50)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    avaliation = models.IntegerField(default=0)

class BookRental(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    price = models.IntegerField()
    
    def __str__(self):
        return f"{self.client}, you rent the book {self.book} for the price {self.price}"