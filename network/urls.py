
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    #development test
    path("test", views.test, name="test"),
    

    # API Routes
    path("post", views.post, name="post"),
    path("feed/<str:section>", views.feed, name="feed"),
    path("profile/", views.own_profile, name="own_profile"),
    path("profile/<int:profile_id>", views.user_profile, name="user_profile"),
]
