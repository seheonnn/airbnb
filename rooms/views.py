from django.shortcuts import render

from .models import Room

# def see_all_rooms(request):
#     rooms = Room.objects.all()
#     # render(request, 템플릿 이름, 보낼 데이터 딕셔너리 {"이름":값})
#     return render(request,"all_rooms.html",{"rooms": rooms,"title": "Hello! this title comes from django",},)
#
# def see_one_room(request, room_pk): # url에서 파라미터 넘기면 받는 자리 필요함
#     try:
#         room = Room.objects.get(pk=room_pk)
#         return render(request,"room_detail.html",{"room": room,},)
#     except Room.DoesNotExist:
#         return render(request,"room_detail.html",{"not_found":True,},)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT


from .models import Amenity
from .serializers import AmenitySerializer

# api/v1/rooms/amenities
class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(AmenitySerializer(amenity).data)
        else:
            return Response(serializer.errors)
# api/v1/rooms/amenities/1
class AmenityDetail(APIView):

    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound
    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def post(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity, data=request.data, partial=True) # DB 내 업데이트 대상, 사용자가 보낸 data, partial=
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(AmenitySerializer(updated_amenity).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)
