from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.exceptions import NotFound

from .models import Category
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import CategorySerializer
# ==================================== 1 djang rest framework 사용 x =======================================
# def categories(request):
#     all_categories = Category.objects.all()
#     return JsonResponse(
#         {
#             'ok':True,
#             'categories': serializers.serialize("json", all_categories),
#         }
#     )

# ==================================== 2 djang rest framework 사용 방식 1 =======================================
@api_view(["GET", "POST"]) # GET, POST 방식 모두 허용
def categories(request):
        if request.method == "GET":
            all_categories = Category.objects.all()
            serializer = CategorySerializer(all_categories, many=True)
            return Response(serializer.data)
        elif request.method == "POST":
            serializer = CategorySerializer(data=request.data) # user가 보낸 데이터를 번역하려면 data= 사용
            # print(serializers.is_valid()) # .is_valid() 는 유효성 검사
            # print(serializers.errors)
            # return Response({"created":True})
            if serializer.is_valid():
                new_category = serializer.save() # save() 실행 하면 create() 메소드 실행
                return Response(CategorySerializer(new_category).data)
            else:
                return Response(serializers.errors)



@api_view(["GET", "PUT"])
def category(request, pk):
    if request.method == "GET":
        try:
            category = Category.objects.get(pk=pk)
            serializers = CategorySerializer(category)  # 카테고리 하나만 찾기 때문에 many= 필요 없음, DB에서 넘어오는 첫 번째 인스턴스 번역
            return Response(serializers.data)
        except Category.DoesNotExist:
            raise NotFound
    elif request.method == "PUT":
        category = Category.objects.get(pk=pk)


# Create your views here.
