from django.contrib import admin
from .models import Room, Amenity

# 관리자 패널 action 추가
@admin.action(description="Set all price to zero")
def reset_prices(model_admin, request, rooms): # 매개변수 3개
    # print(model_admin)
    # print(dir(request.user))
    # print(queryset.filter)
    for room in rooms.all():
        room.price = 0
        room.save()

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    actions = (reset_prices, )

    list_display = (
        "name",
        "price",
        "kind",
        "total_amenities", # 관리자 패널에 메소드 반영
        "rating",
        "owner",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "country",
        "city",
        "toilets",
        "pet_friendly",
        "kind",
        "amenities",
        "created_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    # 관리자 패널에서만 사용하면 admin.py에 추가해도 됨
    # def total_amenities(self, room):
    #     return room.amenities.count()

    # 관리자 패널에 검색 기능 추가
    # default는 __contains로 검색
    search_fields = (
        "name",
        "^price",
        # "^name", # __startswith
        # "=price", # 100% 동일한 값 검색

        "=owner__username", # owner -> User.username 으로 검색, ^, = 모두 적용 가능
    )

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )

# Register your models here.
