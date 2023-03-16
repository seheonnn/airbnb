from strawberry.types import Info
from rooms import models

# V1
# def get_all_rooms():
# V2
# def get_all_rooms(info: Info): # info를 받아옴으로써 권한 확인 가능
#     if info.context.request.user.is_authenticated:
#         return models.Room.objects.all()
#     else:
#         raise Exception("Not Auth.")

# V3 schema.py에 permission_classes=[OnlyLoggedIn] 추가
def get_all_rooms():
    return models.Room.objects.all()

def get_room(pk:int):
    try:
        return models.Room.objects.get(pk=pk)
    except:
        return None