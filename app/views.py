from django.shortcuts import render
from .models import *


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

    if books_read == 1:
        result = f"{books_read} book read"
    else:
        result = f"{books_read} books read"

    context["profile"] = profile
    context["result"] = result
    return render(request, "profile.html", context)
