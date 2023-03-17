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
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT

from categories.models import Category

from .models import Amenity
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer

from django.db import transaction

from django.conf import settings

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

    def put(self, request, pk):
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

from rest_framework.permissions import IsAuthenticatedOrReadOnly
# IsAutheticatedOrReadOnly는 만약 요청이 GET이라면 누구나 통과할 수 있게 해줌. 하지만 만약 요청이 POST, PUT, DELETE라면 오직 인증받는 사람들만 통과할 수 있음.
class Rooms(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, many=True, context={'request':request})
        return Response(serializer.data)

    def post(self, request):
        # if request.user.is_authenticated: # permission_classes 추가하면서 삭제
        serializer = RoomDetailSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category") # category id를 user에서 넘겨주면
            if not category_pk:
                raise ParseError("Category is required")
            try:
                category = Category.objects.get(pk=category_pk) # 해당 id로 category object 찾음
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("The category kind should be rooms")
            except Category.DoesNotExist:
                raise ParseError("Category not found")
            try:
                with transaction.atomic():  # error 하나라도 발생하면 DB에 반영 x, pk 낭비 줄일 수 있음
                    room = serializer.save(owner=request.user, category=category)  # room이 가지고 있는 필드인 owner=로 해야 함, serializer가 owner도 **validated_data로 넣음
                    amenities = request.data.get("amenities")
                    for amenity_pk in amenities:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        room.amenities.add(amenity)  # amenity를 찾으면 해당 room에 하나씩 추가. ManyToMany이기 때문
                    serializer = RoomDetailSerializer(room)
                    return Response(serializer.data)
            except Exception:
                raise ParseError("Amenity not found")
        else:
            return Response(serializer.errors)
        # else:
        #     raise NotAuthenticated


class RoomDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room, context={'request':request}) # context= 를 통해 데이터를 직접 넘길 수도 있음
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)
        # if not request.user.is_authenticated:  # 로그인 여부 확인
        #     raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied

        serializer = RoomDetailSerializer(room, data=request.data, partial=True)

        if serializer.is_valid():
            category_pk = request.data.get("category")
            if category_pk:
                try:
                    category = Category.objects.get(pk=category_pk)
                    updated_room = serializer.save(category=category)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be rooms")
                except Category.DoesNotExist:
                    raise ParseError("Category not found")
            else:
                updated_room = serializer.save()
            try:
                with transaction.atomic():  # error 하나라도 발생하면 DB에 반영 x, pk 낭비 줄일 수 있음
                    amenities = request.data.get("amenities")
                    if amenities:
                        updated_room.amenities.clear()
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            updated_room.amenities.add(amenity)  # amenity를 찾으면 해당 room에 하나씩 추가. ManyToMany이기 때문
                    serializer = RoomDetailSerializer(updated_room)
                    return Response(serializer.data)
            except Exception:
                raise ParseError("Amenity not found")
        else:
            return Response(serializer.errors)


    def delete(self, request, pk):
        room = self.get_object(pk)
        # if not request.user.is_authenticated: # 로그인 여부 확인
        #     raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)

from reviews.serializers import ReviewSerializer
class RoomReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            return NotFound
    def get(self, request, pk):
        try:
            # print(request.query_params)
            page = request.query_params.get('page', 1) # default = 1
            # print(type(page))
            page = int(page)
        except ValueError:
            page = 1 # page가 숫자가 아닌 값이 들어오면 page=1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk)
        serializer = ReviewSerializer(
            room.reviews.all()[start:end], # start에서 end-1까지만 반환
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(user=request.user, room=self.get_object(pk)) # 사용자에게 user 정보와 room 정보는 따로 받아오지 않음
            serializer = ReviewSerializer(review)
            return Response(serializer.data)



class RoomAmenities(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            return NotFound
    def get(self, request, pk):
        try:
            page = request.query_params.get('page', 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk)
        serializer = AmenitySerializer(room.amenities.all()[start:end], many=True,)
        return Response(serializer.data)

from medias.serializers import PhotoSerializer

class RoomPhotos(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound
    def post(self, request, pk):
        room = self.get_object(pk)
        # if not request.user.is_authenticated:
        #     raise NotAuthenticated
        if request.user != room.owner:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room) # 사용자로부터 받는 validated_data에는 file과 description 만 있기 때문에 room 따로 지정
                                                # -> PhotoSerializer 참고
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
