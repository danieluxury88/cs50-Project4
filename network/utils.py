from django.db import IntegrityError

from .models import User, Post, Reaction, Follower
from .constants import *


def get_post():
    return Post.objects.first()


def get_all_users():
    return User.objects.all()


def create_post(user, content):
    post = Post(author=user, content=content)
    post.save()
    return post


def is_post_author(post, user):
    post = Post.objects.get(id=post.id)
    return post.author == user


def edit_post(post, user, content):
    post = Post.objects.get(id=post.id)
    if is_post_author(post, user):
        post.content = content
        post.save()
    return post


def get_all_posts():
    return Post.objects.all()


def get_all_user_posts(user):
    return list(Post.objects.filter(author=user))


# Reactions

def check_if_user_already_reacted_same_way_on_post(user, post, value):
    return Reaction.objects.filter(post=post, author=user, value=value).exists()


def check_if_user_already_reacted_on_post(user, post):
    return Reaction.objects.filter(post=post, author=user).exists()


def toggle_reaction(post, user, value):
    reaction = Reaction.objects.get(author=user, post=post)
    reaction.value = value
    reaction.save()


def react_positive_on_post(user, post):
    if not check_if_user_already_reacted_same_way_on_post(user, post, LIKE):
        if check_if_user_already_reacted_on_post(user, post):
            toggle_reaction(post, user, LIKE)
        else:
            reaction = Reaction(post=post, author=user, value=LIKE)
            reaction.save()


def react_negative_on_post(user, post):
    if not check_if_user_already_reacted_same_way_on_post(user, post, DISLIKE):
        if check_if_user_already_reacted_on_post(user, post):
            toggle_reaction(post, user, DISLIKE)
        else:
            reaction = Reaction(post=post, author=user, value=DISLIKE)
            reaction.save()


def get_all_post_reactions(post):
    return Reaction.objects.filter(post=post)


def get_all_post_id_reactions(post_id):
    return Reaction.objects.filter(id=post_id)


def count_all_positive_post_reactions(post):
    return Reaction.objects.filter(post=post, value=LIKE).count()


def count_all_negative_post_reactions(post):
    return Reaction.objects.filter(post=post, value=DISLIKE).count()


# Followers

def follow_user(user, follower):
    if user != follower:
        follow = Follower(user=user, follower=follower)
        follow.save()


def get_all_followers(user_id):
    return Follower.objects.filter(user=user_id)


def get_all_following(user_id):
    return Follower.objects.filter(follower=user_id)


def get_all_posts_from_following(user_id):
    following_users = get_all_following(user_id)
    users = [followed_user.user for followed_user in following_users ]
    posts =[]
    for user in users:
        posts.append(get_all_user_posts(user))

    flattened_posts = [post for sublist in posts for post in sublist]
    return flattened_posts

