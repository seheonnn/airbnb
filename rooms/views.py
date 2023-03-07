from django.shortcuts import render
from django.http import HttpResponse
from .models import Room

def see_all_rooms(request):
    rooms = Room.objects.all()
    # render(request, 템플릿 이름, 보낼 데이터 딕셔너리 {"이름":값})
    return render(
        request,
        "all_rooms.html",
        {
            "rooms": rooms,
            "title": "Hello! this title comes from django",
        },
    )

def see_one_room(request, room_pk): # url에서 파라미터 넘기면 받는 자리 필요함
    try:
        room = Room.objects.get(pk=room_pk)
        return render(
            request,
            "room_detail.html",
            {
                "room": room,
            },
        )
    except Room.DoesNotExist:
        return render(
            request,
            "room_detail.html",
            {
                "not_found":True,
            },
        )

# Create your views here.
