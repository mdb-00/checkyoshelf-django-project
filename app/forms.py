from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class BookshelfForm(ModelForm):
    class Meta:
        model = Bookshelf
        fields = "__all__"


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = "__all__"


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
