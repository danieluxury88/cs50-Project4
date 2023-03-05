from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt

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
        if request.method == "GET":
            return JsonResponse([post.serialize() for post in posts], safe=False)
    if (section == 'following'):
        user = request.user
        posts = get_all_posts_from_following(user)
        if request.method == "GET":
            return JsonResponse([post.serialize() for post in posts], safe=False)


def own_profile(request):
    username = model_to_dict(request.user)
    following = str(get_all_following(request.user).count())
    followers = str(get_all_followers(request.user).count())
    data = {'username': request.user.email, 'following': following, 'followers':followers}

    if request.method == "GET":
        return JsonResponse(data, safe=False)
    

def user_profile(request, profile_id):    
    posts = get_all_user_posts(request.user)
    if request.method == "GET":
        return JsonResponse([post.serialize() for post in posts], safe=False)

def test(request):
    one_post = get_post()
    return JsonResponse(one_post.serialize())


