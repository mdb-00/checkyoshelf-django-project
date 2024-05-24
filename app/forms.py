from django.forms import ModelForm, Textarea
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class CreateProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"


class BookshelfForm(ModelForm):
    class Meta:
        model = Bookshelf
        fields = "__all__"
        # widgets = {
        #     "profile": Textarea(attrs={"rows": 5}),
        # }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("profile", None)
        super(BookshelfForm, self).__init__(*args, **kwargs)
        my_profile = Profile.objects.get(user=user)
        print("checking if this prints")
        self.fields["profile"].initial = my_profile


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = "__all__"


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = "__all__"


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = "__all__"


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
