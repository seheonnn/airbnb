from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room
from users.serializer import TinyUserSerializer
from categories.serializers import CategorySerializer



# class RoomSerializer(ModelSerializer):
#     class Meta:
#         model = Room
#         fields = "__all__"
#         depth = 1 # owner에 userid가 들어가는 것이 아닌 user object가 들어감 -> 데이터가 너무 많아짐


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = "name", "description"

class RoomDetailSerializer(ModelSerializer):

    owner = TinyUserSerializer(read_only=True)
    amenities = AmenitySerializer(read_only=True, many=True) # amenity 여러 개 many= 추가
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Room
        fields = "__all__"
        # depth=1

class RoomListSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
        )
