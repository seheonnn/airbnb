from rest_framework import serializers

from experiences.models import Experience
from rooms.models import Room
from .models import Review
from users.serializers import TinyUserSerializer

class ReviewSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer(read_only=True) # 리뷰 생성 시에 유저에게 유저 정보를 묻지 않고 알아서 가져오기 때문
    class Meta:
        model = Review
        fields = ("user", "payload", "rating")


class UserReviewSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ("name", "rating", "payload")

    def get_name(self, review):
        if review.room:
            name = Room.objects.get(name=review.room).name
        else:
            name = Experience.objects.get(name=review.experience).name
        return name

