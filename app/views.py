from django.shortcuts import render
from .models import *


# Create your views here.
def home_view(request):
    return render(request, "home.html")
