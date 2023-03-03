from enum import Enum


class UserType(Enum):
    SUPERUSER = 1
    USER = 2
    GUEST = 3


LIKE = 1
DISLIKE = -1
REACTION_TYPE_CHOICES = (
    (LIKE, 'like'),
    (DISLIKE, 'dislike'),
)
