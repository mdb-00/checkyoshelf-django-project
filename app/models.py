from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    followers = []
    following = []

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Book(models.Model):
    GENRES = (
        ("Horror", "Horror"),
        ("Fantasy", "Fantasy"),
        ("Sci-Fi", "Sci-Fi"),
        ("Thriller", "Thriller"),
        ("Mystery", "Mystery"),
    )
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    profile = models.ManyToManyField(Profile, blank=True)
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=200, choices=GENRES)
    synopsis = models.TextField()
    cover = models.CharField(max_length=200, null=True, blank=True)
    page_number = models.IntegerField()
    publish_date = models.DateField()
    reviewers = []
    average_rating = 0.0

    def __str__(self):
        return self.title


class Bookshelf(models.Model):
    profile = models.ManyToManyField(Profile, related_name="profile", blank=True)
    books = models.ManyToManyField(Book, blank=True, related_name="books")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    profile = models.ManyToManyField(Profile)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    text = models.TextField()
    date = models.DateField()
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], default=0
    )
    likes = 0

    def __str__(self):
        return f"{self.rating} star review | {self.book.title}"


class Post(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True
    )
    text = models.TextField()
    date = models.DateField(null=True, blank=True)
    likes = 0
    times_shared = 0

    def __str__(self):
        return f"{self.profile.user.username}'s post"


class Comment(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    date = models.DateField(null=True, blank=True)
    likes = 0
    times_shared = 0

    def __str__(self):
        return f"{self.profile.user.username}'s comment"
