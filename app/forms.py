from django.forms import ModelForm
from .models import *


class BookshelfForm(ModelForm):
    class Meta:
        model = Bookshelf
        fields = "__all__"


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = "__all__"
