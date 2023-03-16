import strawberry
from strawberry import auto
from users.models import User

@strawberry.django.type(User)
class UserType:
    name: auto
    email: auto
    username: auto