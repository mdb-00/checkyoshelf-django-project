from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Profile)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Bookshelf)
