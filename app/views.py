from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import *
from .forms import *
from .decorators import *


# Create your views here.
def default_bookshelves():
    # shelf_names = ["All", "Read", "Currently Reading", "Want to Read"]
    profiles = Profile.objects.all()
    # bookshelves = []

    for profile in profiles:
        shelf_exists = Bookshelf.objects.filter(profile=profile, name="All").exists()
        if shelf_exists == False:
            Bookshelf.objects.create(profile=profile, name="All")

        # for name in shelf_names:
        #     shelf_exists = Bookshelf.objects.filter(profile=profile, name=name).exists()
        #     if shelf_exists == False:
        #         bookshelf = Bookshelf.objects.create(profile=profile, name=name)
        #         bookshelves.append(bookshelf)


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
def explore_view(request):
    context = {}

    default_bookshelves()
    current_user = request.user
    my_profile = Profile.objects.get(user=current_user)
    genres = Genre.objects.all()

    created_bookshelves = Bookshelf.objects.filter(profile=my_profile).exclude(
        name="All"
    )

    books_by_genres = {}

    for genre in genres:
        books = Book.objects.filter(genre=genre)
        for book in books:
            books_by_genres[genre] = books

    context["current_user"] = current_user
    context["my_profile"] = my_profile
    context["books_by_genres"] = books_by_genres
    context["created_bookshelves"] = created_bookshelves
    return render(request, "explore.html", context)


@login_required(login_url="login")
def profile_view(request, username):
    context = {}

    current_user = request.user
    my_profile = Profile.objects.get(user=current_user)

    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        posts = Post.objects.filter(profile=profile)
        bookshelf = Bookshelf.objects.get(profile=profile, name="All")
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
        result = f"{books_read} book"
    else:
        result = f"{books_read} books"

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

    default_bookshelves = Bookshelf.objects.filter(profile=profile).filter(
        Q(name="All")
        # | Q(name="Read")
        # | Q(name="Currently Reading")
        # | Q(name="Want to Read")
    )

    created_bookshelves = Bookshelf.objects.filter(profile=profile).exclude(
        Q(name="All")
        # | Q(name="Read")
        # | Q(name="Currently Reading")
        # | Q(name="Want to Read")
    )
    default_bookshelves_count = {}
    created_bookshelves_count = {}

    for shelf in default_bookshelves:
        shelf_books = shelf.books.all()
        default_bookshelves_count[shelf] = shelf_books.count()

    for shelf in created_bookshelves:
        shelf_books = shelf.books.all()
        created_bookshelves_count[shelf] = shelf_books.count()

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
    context["default_bookshelves_count"] = default_bookshelves_count
    context["created_bookshelves_count"] = created_bookshelves_count
    return render(request, "bookshelves.html", context)


def remove_book_from_shelf(request, book, shelf):
    current_user = request.user
    my_profile = Profile.objects.get(user=current_user)

    bookshelf = Bookshelf.objects.get(name=shelf, profile=my_profile)
    all_bookshelf = Bookshelf.objects.get(name="All", profile=my_profile)
    book_obj = Book.objects.get(title=book)
    book_obj.status = shelf
    book_obj.save()
    bookshelf.books.remove(book_obj)
    all_bookshelf.books.remove(book_obj)

    bookshelf.save()
    all_bookshelf.save()
    return redirect(f"/{current_user}/bookshelves")


def add_book_to_shelf(request, book, shelf):
    current_user = request.user
    my_profile = Profile.objects.get(user=current_user)

    bookshelf = Bookshelf.objects.get(name=shelf, profile=my_profile)
    all_bookshelf = Bookshelf.objects.get(name="All", profile=my_profile)
    book_obj = Book.objects.get(title=book)
    book_obj.status = shelf
    book_obj.save()
    bookshelf.books.add(book_obj)
    all_bookshelf.books.add(book_obj)

    bookshelf.save()
    all_bookshelf.save()
    return redirect(f"/{current_user}/{shelf}/books")


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

    default_bookshelves = Bookshelf.objects.filter(profile=profile).filter(
        Q(name="All")
        # | Q(name="Read")
        # | Q(name="Currently Reading")
        # | Q(name="Want to Read")
    )

    created_bookshelves = Bookshelf.objects.filter(profile=profile).exclude(
        Q(name="All")
        # | Q(name="Read")
        # | Q(name="Currently Reading")
        # | Q(name="Want to Read")
    )
    default_bookshelves_count = {}
    created_bookshelves_count = {}

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
    context["selected_bookshelf"] = selected_bookshelf
    context["bookshelves_count"] = bookshelves_count
    context["books_ratings"] = books_ratings
    context["default_bookshelves_count"] = default_bookshelves_count
    context["created_bookshelves_count"] = created_bookshelves_count
    return render(request, "books.html", context)


@login_required(login_url="login")
def create_bookshelf(request, username):
    context = {}

    current_user = request.user
    my_profile = Profile.objects.get(user=current_user)

    form = BookshelfForm(profile=current_user)

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
    all_bookshelf = Bookshelf.objects.get(profile=my_profile, name="All")
    books = bookshelf.books.all()

    for book in books:
        book_obj = Book.objects.get(title=book)
        bookshelf.books.remove(book_obj)
        all_bookshelf.books.remove(book_obj)
        bookshelf.save()
        all_bookshelf.save()

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


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def user_view(request):
    users = User.objects.exclude(username=request.user)
    user_profiles = {}

    for user in users:
        user_profiles[user] = Profile.objects.get(user=user)

    context = {"user_profiles": user_profiles}
    return render(request, "user_management.html", context)


def delete_user(request, username):
    user = User.objects.get(username=username)
    user.delete()
    return redirect("user_management")
