from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models

from . import constants

import time


class User(AbstractUser):
    class UserType(models.TextChoices):
        SUPERUSER = 'SU', _('Superuser')
        USER = 'US', _('User')
        GUEST = 'GE', _('Guest')

    email = models.EmailField(unique=True)
    native_name = models.CharField(max_length=5)
    phone_no = models.CharField(max_length=10)
    user_type = models.CharField(max_length=2, choices=UserType.choices, default=UserType.USER)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return "{}".format(self.email)



class Post(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.author} said: {self.content} on {self.timestamp.strftime("%d-%m-%Y %H:%M:%S")} (edited:{self.edited})'

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.email,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }


class Reaction(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="writer")
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="reactions")
    value = models.IntegerField(choices=constants.REACTION_TYPE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Add a unique constraint on the user and post fields to ensure that a user can only react once to a post
        unique_together = ('post', 'author')

    def __str__(self):
        return f'{self.author} reacted: {self.value} on {self.post.content} by {self.post.author}'


class Follower(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")

    def __str__(self):
        return f'{self.user} is being followed by {self.follower}'