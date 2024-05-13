from django.shortcuts import render
from .models import *


# Create your views here.
def home_view(request):
    return render(request, "home.html")


def profile_view(request, username):
    context = {}
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    context["profile"] = profile
    return render(request, "profile.html", context)
