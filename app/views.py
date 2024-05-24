from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from .decorators import *


# Create your views here.
def default_bookshelves():
    shelf_names = ["All", "Read", "Currently Reading", "Want to Read"]
    profiles = Profile.objects.all()
    bookshelves = []

    for profile in profiles:
        for name in shelf_names:
            shelf_exists = Bookshelf.objects.filter(profile=profile, name=name).exists()
            if shelf_exists == False:
                bookshelf = Bookshelf.objects.create(profile=profile, name=name)
                bookshelves.append(bookshelf)


@unauthenticated_user
def register_view(request):
    form = CreateUserForm

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("create_profile")

    context = {"form": form}
    return render(request, "register.html", context)


@unauthenticated_user
def create_profile(request):
    form = CreateProfileForm

    if request.method == "POST":
        form = CreateProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")

    context = {"form": form}
    return render(request, "profile_form.html", context)


@unauthenticated_user
def login_view(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def home_view(request):
    context = {}
    default_bookshelves()
    current_user = request.user
    my_profile = Profile.objects.get(user=current_user)

    context["current_user"] = current_user
    context["my_profile"] = my_profile
    return render(request, "home.html", context)


@login_required(login_url="login")
def profile_view(request, username):
    context = {}

    current_user = request.user
    my_profile = Profile.objects.get(user=current_user)

    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        posts = Post.objects.filter(profile=profile)
        bookshelf = Bookshelf.objects.get(profile=profile, name="Read")
        read_books = bookshelf.books.all()
        books_read = read_books.count()
        follower_count = len(profile.followers)
        following_count = len(profile.following)
    except:
        user = None
        profile = None
        posts = None
        bookshelf = None
        read_books = None
        books_read = 0
        follower_count = 0
        following_count = 0

    result = ""

    if books_read == 1:
        result = f"{books_read} book read"
    else:
        result = f"{books_read} books read"

    context["current_user"] = current_user
    context["my_profile"] = my_profile
    context["user"] = user
    context["profile"] = profile
    context["result"] = result
    context["follower_count"] = follower_count
    context["following_count"] = following_count
    context["posts"] = posts
    return render(request, "profile.html", context)


@login_required(login_url="login")
def bookshelf_view(request, username):
    context = {}

    current_user = request.user
    my_profile = Profile.objects.get(user=current_user)

    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
    except:
        user = None
        profile = None

    bookshelves = Bookshelf.objects.filter(profile=profile)
    bookshelves_count = {}

    for shelf in bookshelves:
        shelf_books = shelf.books.all()
        bookshelves_count[shelf] = shelf_books.count()

    # bookshelves_count = {
    #     key: value for key, value in sorted(unsorted_bookshelves.items())
    # }

    # bookshelves_count = {
    #     k: v for k, v in sorted(unsorted_bookshelves.items(), key=lambda item: item[0])
    # }

    context["current_user"] = current_user
    context["my_profile"] = my_profile
    context["user"] = user
    context["profile"] = profile
    context["bookshelves_count"] = bookshelves_count
    return render(request, "bookshelves.html", context)


@login_required(login_url="login")
def books_view(request, username, bookshelf):
    context = {}

    current_user = request.user
    my_profile = Profile.objects.get(user=current_user)

    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
    except:
        user = None
        profile = None

    bookshelves = Bookshelf.objects.filter(profile=profile)
    bookshelves_count = {}

    for shelf in bookshelves:
        shelf_books = shelf.books.all()
        bookshelves_count[shelf] = shelf_books.count()

    selected_bookshelf = Bookshelf.objects.get(profile=profile, name=bookshelf)
    books = selected_bookshelf.books.all()
    books_ratings = {}

    for book in books:
        try:
            review = Review.objects.get(book=book)
            books_ratings[book] = [book.average_rating, review.rating]
        except:
            review = None
            books_ratings[book] = [book.average_rating, "-"]

    context["current_user"] = current_user
    context["my_profile"] = my_profile
    context["profile"] = profile
    context["bookshelves_count"] = bookshelves_count
    context["books_ratings"] = books_ratings
    return render(request, "books.html", context)


@login_required(login_url="login")
def create_bookshelf(request, username):
    context = {}

    current_user = request.user
    my_profile = Profile.objects.get(user=current_user)

    form = BookshelfForm(profile=current_user)

    # field = form.fields['profile']
    # field.widget = field.hidden_widget()

    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
    except:
        user = None
        profile = None

    if request.method == "POST":
        form = BookshelfForm(request.POST, profile=current_user)
        if form.is_valid():
            form.save()
            return redirect(f"/{username}/bookshelves")

    context["current_user"] = current_user
    context["my_profile"] = my_profile
    context["profile"] = profile
    context["form"] = form
    return render(request, "bookshelf_form.html", context)


@login_required(login_url="login")
def review_book(request, username, book):
    context = {}

    form = ReviewForm()

    current_user = request.user
    my_profile = Profile.objects.get(user=current_user)

    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
    except:
        user = None
        profile = None

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f"/{username}/bookshelves")

    context["current_user"] = current_user
    context["my_profile"] = my_profile
    context["profile"] = profile
    context["form"] = form
    return render(request, "review_form.html", context)


@login_required(login_url="login")
def make_post(request, username):
    context = {}

    form = PostForm()

    current_user = request.user
    my_profile = Profile.objects.get(user=current_user)

    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
    except:
        user = None
        profile = None

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f"/{username}")

    context["current_user"] = current_user
    context["my_profile"] = my_profile
    context["profile"] = profile
    context["form"] = form
    return render(request, "post_form.html", context)


@login_required(login_url="login")
def delete_bookshelf(request, username, shelf):
    current_user = request.user
    my_profile = Profile.objects.get(user=current_user)
    bookshelf = Bookshelf.objects.get(profile=my_profile, name=shelf)
    bookshelf.delete()
    return redirect(f"/{username}/bookshelves")


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def add_author(request):
    form = AuthorForm

    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()

    context = {"form": form}

    return render(request, "author_form.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def add_books(request):
    form = BookForm

    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()

    context = {"form": form}

    return render(request, "book_form.html", context)


def edit_profile(request):
    current_user = request.user
    profile = Profile.objects.get(user=current_user)

    form = CreateProfileForm(instance=profile)

    if request.method == "POST":
        form = CreateProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(f"/{current_user}")

    context = {"form": form}
    return render(request, "profile_form.html", context)
