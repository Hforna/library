from rest_framework import serializers
from library_app.models import Book
from django.contrib.auth.models import User


class Books(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["book_name", "owner", "gender", "price_rent", "description", "images", "number_visit_page", "user_detail"]
    
    user_detail = serializers.HyperlinkedRelatedField(source="owner", view_name="user_detail", read_only=True)

class UserBook(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]
    

    
    
