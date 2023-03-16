import strawberry
from strawberry import auto
from strawberry.types import Info
from rooms.models import Room
from wishlists.models import Wishlist

from config.strawberryGraphQL.users.types import UserType
from config.strawberryGraphQL.reviews.types import ReviewType
import typing


@strawberry.django.type(Room)
class RoomType:
    id: auto
    name: auto # auto는 알아서 model로 가서 type 가져옴, model에 있는 field들과 이름 같아야 함.
    kind: auto
    owner: "UserType"

    @strawberry.field
    # def reviews(self, page: int) -> typing.List["ReviewType"]:
    def reviews(self, page:typing.Optional[int] = 1) -> typing.List["ReviewType"]:
        from config import settings
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        return self.reviews.all()[start:end]

    @strawberry.field
    def rating(self) -> str:
        return self.rating()

    @strawberry.field # Info에 request 정보가 담겨있음
    def is_owner(self, info: Info) -> bool:
        return self.owner == info.context.request.user
    @strawberry.field
    def is_liked(self, info: Info) -> bool:
        return Wishlist.objects.filter(user=info.context.request.user, rooms__pk=self.pk).exists()


# GraphQL relationships
# {
#   allRooms{
#     id
#     name
#     kind
#     owner {
#       username
#     }
#   }
# }