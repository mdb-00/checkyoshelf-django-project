from django.forms import ModelForm
from .models import *

class BookshelfForm(ModelForm):
    class Meta:
        model = Bookshelf
        fields = "__all__"
        