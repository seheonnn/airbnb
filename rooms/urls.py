from django.urls import path
from rooms import views

urlpatterns = [
    path("", views.see_all_rooms), # 이미 rooms/로 들어온 것이기 때문에 "" 비어있음
    # <넘길 파라미터 타임 : 넘길 파라미터 이름>
    path("<int:room_pk>", views.see_one_room),
]