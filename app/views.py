from django.shortcuts import render, redirect
from .models import *
from .forms import *


# Create your views here.
def home_view(request):
    return render(request, "home.html")


def profile_view(request, username):
    context = {}

    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        bookshelf = Bookshelf.objects.get(profile=profile, name="Read")
    except:
        user = None
        profile = None
        bookshelf = None

    result = ""
    read_books = bookshelf.books.all()
    books_read = read_books.count()

    follower_count = len(profile.followers)
    following_count = len(profile.following)

    if books_read == 1:
        result = f"{books_read} book read"
    else:
        result = f"{books_read} books read"

    context["profile"] = profile
    context["result"] = result
    context["follower_count"] = follower_count
    context["following_count"] = following_count
    return render(request, "profile.html", context)


def bookshelf_view(request, username):
    context = {}

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

    context["profile"] = profile
    context["bookshelves_count"] = bookshelves_count
    return render(request, "bookshelves.html", context)


def books_view(request, username, bookshelf):
    context = {}

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

    selected_bookshelf = Bookshelf.objects.get(name=bookshelf)
    books = selected_bookshelf.books.all()
    books_ratings = {}
    has_rating = True

    for book in books:
        try:
            review = Review.objects.get(book=book)
            books_ratings[book.title] = book.average_rating, review.rating
        except:
            has_rating = False
            review = None
            books_ratings[book.title] = book.average_rating

    context["profile"] = profile
    context["bookshelves_count"] = bookshelves_count
    context["books_ratings"] = books_ratings
    context["has_rating"] = has_rating
    return render(request, "books.html", context)


def create_bookshelf(request, username):
    context = {}

    form = BookshelfForm()

    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
    except:
        user = None
        profile = None

    if request.method == "POST":
        form = BookshelfForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f"/{username}/bookshelves")

    context["profile"] = profile
    context["form"] = form
    return render(request, "bookshelf_form.html", context)


def review_book(request, username, book):
    context = {}

    form = ReviewForm()

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

    context["profile"] = profile
    context["form"] = form
    return render(request, "review_form.html", context)
