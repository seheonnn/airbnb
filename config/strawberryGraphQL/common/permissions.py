from strawberry.types import Info
import typing
from strawberry.permission import BasePermission

class OnlyLoggedIn(BasePermission):

    message = "You need to be logged in for this!" # 권한 없는 user에게 보여주는 메세지

    def has_permission(self, source: typing.Any, info: Info):
        return info.context.request.user.is_authenticated