"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", root, name="root"),
    path("", home_view, name="home"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("<str:username>/", profile_view, name="profile"),
    path("<str:username>/bookshelves", bookshelf_view, name="bookshelves"),
    path("<str:username>/<str:bookshelf>/books", books_view, name="books"),
    path("<str:username>/create-bookshelf/", create_bookshelf, name="create_bookshelf"),
    path("<str:username>/review-book/<str:book>/", review_book, name="review_book"),
    path(
        "<str:username>/<str:shelf>/delete/", delete_bookshelf, name="delete_bookshelf"
    ),
]
