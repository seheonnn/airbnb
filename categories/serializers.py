from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.Serializer):

    # Category 모델의 내용
    pk = serializers.IntegerField(read_only=True) # read_only=True 인 값은 user가 보낼 필요 없음
    name = serializers.CharField(required=True, max_length=50,) # max_length 는 validation 임
    kind = serializers.ChoiceField(
        choices=Category.CategoryKindChoices.choices,
    )
    created_at = serializers.DateTimeField(read_only=True)

    # create()는 객체를 return 해야 함.
    def create(self, validated_data):
        return Category.objects.create(
            # 가능하지만 비효율적
            # name=validated_data['name'],
            # kind=validated_data['kind']
            **validated_data
        )