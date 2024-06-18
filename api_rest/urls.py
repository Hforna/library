from django.urls import path
from .api import BookView, UserView

urlpatterns = [
    path("/book_detail", BookView.as_view(), name="book_detail"),
    path("/user_detail/<int:pk>", UserView.as_view(), name="user_detail")
]
