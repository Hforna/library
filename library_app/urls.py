from django.urls import path
from .views import *
from django.shortcuts import redirect

urlpatterns = [
    path("", lambda request: redirect("home")),
    path("home", home, name="home"),
    path("signup", sign_up, name="signup"),
    path("login", loginn, name="login"),
    path("logout", logoutt, name="logout"),
    path("fiction", books_fiction, name="fiction"),
    path("science", books_science, name="science"),
    path("history", books_history, name="history"),
    path("book/<int:pk>", show_book, name="show_book"),
    path("publish_book/<int:pk>", publish_book, name="publish_book"),
    path("exclude_book/<int:pk>", exclude_book, name="exclude_book"),
    path("profile", profile)
]