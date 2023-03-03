from django.contrib.auth.models import AbstractUser
from django.db import models

import time


class User(AbstractUser):
    pass


class Post(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.author} said: {self.content} on {self.timestamp.strftime("%d-%m-%Y %H:%M:%S")} (edited:{self.edited})'


class Reaction(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="writer")
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="reactions")
    value = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} reacted: {self.value} on {self.post.content} by {self.post.author}'


class Follower(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")
    following = models.ManyToManyField("User", related_name="following")

    def __str__(self):
        return f'{self.user} is following {self.following.user}'
