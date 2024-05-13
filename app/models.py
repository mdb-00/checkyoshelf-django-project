from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from typing import List


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    followers = List[str]
    following = List[str]

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    synopsis = models.TextField()
    cover = models.CharField(max_length=200, null=True, blank=True)
    page_number = models.IntegerField()
    publish_date = models.DateField()
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title


class Bookshelf(models.Model):
    profile = models.ManyToManyField(Profile)
    book = models.ManyToManyField(Book, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
