import strawberry
from strawberry import auto
from reviews import models

@strawberry.django.type(models.Review)
class ReviewType:
    id: auto
    payload: auto
    rating: auto