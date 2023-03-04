from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse

from .models import User
from .utils import *


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def index(request):
    posts = get_all_posts()
    context = {'posts': posts}
    return render(request, "network/index.html", context)


def post(request):
    pass


def feed(request, section):
    if (section == 'all'):
        posts = get_all_posts()
        print('all posts')
    else:
        print(request.user)
        # posts = get_all_posts()
        posts = get_all_posts_from_following(request.user)
        print('all posts')

    context = {'posts': posts}
    return render(request, "network/index.html", context)


def profile(request, profile_id):
    print('all posts')
    posts = get_all_user_posts(request.user)
    # context = {'posts': posts}
    # return render(request, "network/index.html", context)

    if request.method == "GET":
        return JsonResponse([post.serialize() for post in posts], safe=False)


