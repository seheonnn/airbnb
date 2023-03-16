import strawberry
import typing
from . import types
from . import queries
from . import mutations
from config.strawberryGraphQL.common.permissions import OnlyLoggedIn


@strawberry.type
class Query:
    all_rooms: typing.List[types.RoomType] = strawberry.field(resolver=queries.get_all_rooms, permission_classes=[OnlyLoggedIn])
    # room: types.RoomType = strawberry.field(resolver=queries.get_room)
    room: typing.Optional[types.RoomType] = strawberry.field(resolver=queries.get_room) # room이 있을 수도 없을 수도

@strawberry.type
class Mutation:
    add_room: typing.Optional[types.RoomType] = strawberry.mutation(resolver=mutations.add_room, permission_classes=[OnlyLoggedIn])