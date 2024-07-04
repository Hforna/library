from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView
from .models import Book, Author, AvaliationsBook
from account.models import Shipping
from django.core.mail import send_mail
from rolepermissions.roles import assign_role, get_user_roles
from rolepermissions.decorators import has_role_decorator
from django.contrib.auth.models import Group, User
from checkout.models import Cart
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.views.generic import ListView
from utils.pagination import make_range_pagination


# Create your views here.

def home(request):
    writer_user = request.user
    if request.user.groups.filter(name="writer").exists():
        if request.method == "POST":
            title = request.POST["title"]
            description = request.POST["description"]
            genre = request.POST["genre"]
            image = request.FILES["cover"]
            price = request.POST["price"]
            book_create = Book.objects.create(owner=request.user, book_name=title, gender=genre, price_rent=price, description=description, images=image)
            book_create.save()
            if Book.objects.filter(book_name=title).exists():
                messages.success(request, "Book created successfully")
                return redirect("home")
            else:
                messages.error(request, "The book has not created")

        books = Book.objects.filter(owner=request.user.id)
        numberr = []
        number_books = 0
        for book in books:
            numberr.append(book)
            if len(numberr) > 0:
                number_books += 1

        try:
            author = Author.objects.get(user_id=request.user.id)
            return render(request, "library_app/home.html", context={'writer_user': writer_user, 'books': books, 'number_books': number_books, 'author': author})
        except ObjectDoesNotExist:
            messages.error(request, "You need update your profile")
            return render(request, "library_app/home.html", context={'writer_user': writer_user, 'books': books, 'number_books': number_books})
    else:
        books = Book.objects.all()
        order_book = []
        for book in books:
            order_book.append([book.number_visit_page, book.id])
        list_max = order_book
        order_list = sorted(list_max, key=lambda x: x[0], reverse=True)
        books_filter = []
        try:
            for n in range(5):
                lists = order_list[n]
                books_filter.append(Book.objects.filter(id=lists[1]))
            number = -1
            for x in books_filter:
                number += 1
                books_filter[number] = x
            final_book = books_filter           
        except Exception:
            if len(order_list) == 1:
                for n in range(len(order_list)):
                    lists = order_list[n]
                    books_filter.append(Book.objects.filter(id=lists[1]))
            else:
                for n in range(1, len(order_list) -1):
                    lists = order_list[n]
                    books_filter.append(Book.objects.filter(id=lists[1]))
            number = -1
            for x in books_filter:
                number += 1
                books_filter[number] = x
            final_book = books_filter[:len(order_list)]


        return render(request, "library_app/home.html", context={"books_filter": final_book})

@login_required
def profile(request):
    if request.method == "POST":
        full_name = request.POST["full_name"]
        country = request.POST["country"]
        username = request.POST["username"]
        images = request.FILES["profile-pic"]
        
        try:
            edit_author = Author.objects.get(user_id=request.user.id)
            edit_author.full_name = full_name
            edit_author.country = country
            edit_author.images = images
            edit_author.save()
            messages.success(request, "Profile updated")
        except ObjectDoesNotExist:
            create_author = Author.objects.create(user_id=request.user.id, full_name=full_name, country=country, images=images)
        user = User.objects.get(id=request.user.id)
        user.username = username
        user.save()



    try:
        edit_author = Author.objects.get(user_id=request.user.id)
        return render(request, "library_app/profile.html", context={'author_user': edit_author})
    except ObjectDoesNotExist:
        messages.error(request, "You need to update your profile")
        return render(request, "library_app/profile.html")

def sign_up(request):
    if request.user.is_authenticated:
        return redirect("/home")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        role_user = request.POST["role"]
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        if role_user == "writer":
            assign_role(User.objects.get(username=username), 'writer')

        return redirect("/home")
    return render(request, "library_app/signup.html")

def loginn(request):
    if request.user.is_authenticated:
        return redirect("/home")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        user = authenticate(request, username=username, password=password, email=email)
        if user is not None:
            login(request, user)
            messages.success(request, "login success")
            return redirect("/home")
        else:
            messages.error(request, "username or password is incorrect")
    return render(request, "library_app/login.html")

def logoutt(request):
    logout(request)
    return redirect("/home")

def books_fiction(request):
    books = Book.objects.filter(gender="fiction")
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1
    paginator = Paginator(books, 4)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_range_pagination(current_page=current_page, qty_pages=4, page_range=paginator.page_range)

    return render(request, "library_app/fiction.html", context={"books": page_obj, 'pagination_range': pagination_range})

def books_science(request):
    books = Book.objects.filter(gender="science")
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1
    paginator = Paginator(books, 4)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_range_pagination(current_page=current_page, qty_pages=4, page_range=paginator.page_range)
    
    return render(request, "library_app/science.html", context={"books": page_obj, 'pagination_range': pagination_range})

def books_history(request):
    books = Book.objects.filter(gender="history")
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1
    paginator = Paginator(books, 4)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_range_pagination(current_page=current_page, qty_pages=4, page_range=paginator.page_range)

    return render(request, "library_app/history.html", context={"books": page_obj, 'pagination_range': pagination_range})

def show_book(request, pk):
    book = Book.objects.get(pk=pk)
    book.number_visit_page += 1
    book.save()
    if "add_to_cart" in request.POST:
        if request.user.is_authenticated:
            if Cart.objects.filter(user=request.user.id).exists():
                if Cart.objects.filter(user=request.user.id).filter(book=book).exists():                    
                    user_cart = Cart.objects.filter(user=request.user.id).filter(book=book).first()
                    user_cart.quantity += 1
                    user_cart.save()
                else:
                    cart = Cart.objects.create(user=request.user, book=book, quantity=1)
                    cart.save()
            else:
                cart = Cart.objects.create(user=request.user, book=book, quantity=1)
                cart.save()
            return redirect("/checkout/cart")
        else:
            messages.error(request, "you need are logged to add in cart")
            return redirect("login")
    elif "buy_now" in request.POST:
        if request.user.is_authenticated:
            if Cart.objects.filter(user=request.user.id).exists():
                if Cart.objects.filter(user=request.user.id).filter(book=book).exists():
                    user_cart = Cart.objects.filter(user=request.user.id).filter(book=book).first()
                    user_cart.quantity += 1
                    user_cart.save()
                else:
                    cart = Cart.objects.create(user=request.user, book=book, quantity=1)
                    cart.save()
            else:
                cart = Cart.objects.create(user=request.user, book=book, quantity=1)
                cart.save()
            return redirect("/checkout/shipping")
        else:
            messages.error(request, "you need are logged to buy now")
            return redirect("login")
    try:
        avaliation_book = AvaliationsBook.objects.filter(book=book)
    except ObjectDoesNotExist:
        return render(request, "library_app/book.html", context={'book': book})
    
    if "submit_comment" in request.POST:
        userr = request.user
        comment = request.POST["comment"]
        book = Book.objects.get(pk=pk)
        avaliation = request.POST["rating"]
        if request.user.is_authenticated:
            new_avaliation = AvaliationsBook.objects.create(user=userr, comment=comment, book=book, avaliation=avaliation)
        else:
            new_avaliation = AvaliationsBook.objects.create(comment=comment, book=book, avaliation=avaliation)
        new_avaliation.save()
        return redirect(f"/book/{pk}")
        
    return render(request, "library_app/book.html", context={'book': book, 'avaliation_book': avaliation_book})

@has_role_decorator('writer')
def publish_book(request, pk):
    book = Book.objects.get(pk=pk)
    book.is_published = True
    book.save()
    messages.success(request, "Book has published")
    return redirect("home")

@has_role_decorator('writer')
def exclude_book(request, pk):

    book = Book.objects.get(pk=pk)
    book.delete()
    messages.error(request, "Book has deleted")
    return redirect("home")


        
