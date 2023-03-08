from rest_framework import serializers
from .models import Category

# class CategorySerializer(serializers.Serializer):
#
#     # Category 모델의 내용
#     pk = serializers.IntegerField(read_only=True) # read_only=True 인 값은 user가 보낼 필요 없음
#     name = serializers.CharField(required=True, max_length=50,) # max_length 는 validation 임
#     kind = serializers.ChoiceField(
#         choices=Category.CategoryKindChoices.choices,
#     )
#     created_at = serializers.DateTimeField(read_only=True)
#
#     # create()는 객체를 return 해야 함.
#     def create(self, validated_data):
#         return Category.objects.create(
#             # 가능하지만 비효율적
#             # name=validated_data['name'],
#             # kind=validated_data['kind']
#             **validated_data
#         )
#
#
#     def update(self, instance, validated_data): # instance:category의 값, validated_data:사용자 값
#         # 비효율적
#         # if validated_data['name']:
#         #     instance.name = validated_data['name']
#         instance.name = validated_data.get('name', instance.name) # 두 번째 값은 default
#         instance.kind = validated_data.get('kind', instance.kind)
#         instance.save()
#         return instance # create 처럼 객체 return

# ==================== serializers.py V2 ==================================
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category

        # Category의 모든 필드를 다 보여줌
        fields = ("__all__")

        # Category의 필드들 중에서 무엇을 보일지 선택
        # fields = ("name", "kind",)

        # Category의 필드들 중에서 무엇을 숨길지 선택
        # exclude = ("created_at",)

        # 나중에 필요에 따라 create나 update는 수정할 수도 있음