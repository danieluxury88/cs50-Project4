from django.test import TestCase

from .models import User, Post, Reaction, Follower
from .utils import *
from .constants import *


class NetworkTestCase(TestCase):
    user1 = None

    def setUp(self):
        self.user1 = User(username="daniel", email="daniel@test.com", password="test",
                          user_type=User.UserType.SUPERUSER)
        self.user1.save()
        self.user2 = User(username="chiki", email="chiki@test.com", password="test")
        self.user2.save()
        self.user3 = User(username="joha", email="joha@test.com", password="test")
        self.user3.save()

    def test_count_number_of_users(self):
        users = get_all_users()
        self.assertEquals(3, len(users))

    def test_count_number_of_posts(self):
        create_post(self.user1, "Hello World")
        create_post(self.user1, "Hola Mundo")
        posts = get_all_posts()
        self.assertEquals(2, len(posts))

    def test_count_user_posts(self):
        create_post(self.user2, "Hello World")
        create_post(self.user2, "Hello World")
        create_post(self.user2, "Hello World")
        posts = get_all_user_posts(self.user2)
        self.assertEquals(3, len(posts))

    def test_can_edit_post(self):
        post = create_post(self.user1, "Hello World")
        can_edit = is_post_author(post, self.user2)
        self.assertFalse(can_edit)

    def test_edit_post(self):
        post = create_post(self.user1, "Hello World")
        edited_post = edit_post(post, self.user2, "Hola Mundo")
        self.assertNotEquals("Hola Mundo", edited_post.content)
        edited_post = edit_post(post, self.user1, "Hola Mundo")
        self.assertEquals("Hola Mundo", edited_post.content)

    def test_count_only_one_reaction_per_user_per_post(self):
        create_post(self.user1, "Hello World")
        post = Post.objects.first()
        react_positive_on_post(self.user1, post)
        react_positive_on_post(self.user1, post)
        reactions = get_all_post_reactions(post)
        self.assertEquals(1, len(reactions))
        self.assertEquals(1, len(reactions))

    def test_toggle_user_reaction(self):
        create_post(self.user1, "Hello World")
        post = Post.objects.first()
        react_negative_on_post(self.user1, post)
        react_positive_on_post(self.user1, post)
        reactions_count = count_all_positive_post_reactions(post)
        self.assertEquals(1, reactions_count)
        react_negative_on_post(self.user1, post)
        reactions_count = count_all_negative_post_reactions(post)
        self.assertEquals(1, reactions_count)
        reactions_count = count_all_positive_post_reactions(post)
        self.assertEquals(0, reactions_count)

    def test_following_a_user(self):
        follow_user(self.user1, self.user2)
        follow_user(self.user1, self.user3)
        follow_user(self.user2, self.user3)
        followers = get_all_followers(self.user1).count()
        self.assertEquals(2, followers)
        following = get_all_following(self.user1).count()
        self.assertEquals(0, following)
        following = get_all_following(self.user3).count()
        self.assertEquals(2, following)
        followers = get_all_followers(self.user3).count()
        self.assertEquals(0, followers)

    def test_get_all_posts_from_following(self):
        create_post(self.user1, "hola")
        create_post(self.user1, "hello")
        create_post(self.user2, "chao")
        follow_user(self.user1, self.user3)
        follow_user(self.user2, self.user3)
        posts = get_all_posts_from_following(self.user3)
        self.assertEquals(3, len(posts))


