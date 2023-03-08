from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT

from .models import Category
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import CategorySerializer

# 사용자 데이터 (request.data)만으로 serializer를 만들면 create 실행
#  사용자 데이터와 DB에서 가져온 데이터로 serializer를 만들면 update 실행

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
# @api_view(["GET", "POST"]) # GET, POST 방식 모두 허용
# def categories(request):
#         if request.method == "GET":
#             all_categories = Category.objects.all()
#             serializer = CategorySerializer(all_categories, many=True) # category 객체 여러개 many=
#             return Response(serializer.data)
#         elif request.method == "POST": # 카테고리 만들기
#             serializer = CategorySerializer(data=request.data) # user가 보낸 데이터를 번역하려면 data= 사용
#             # print(serializers.is_valid()) # .is_valid() 는 유효성 검사
#             # print(serializers.errors)
#             # return Response({"created":True})
#             if serializer.is_valid():
#                 new_category = serializer.save() # save() 실행 하면 create() 메소드 실행
#                 return Response(CategorySerializer(new_category).data)
#             else:
#                 return Response(serializers.errors)
#
#
#
# @api_view(["GET", "PUT", "DELETE"])
# def category(request, pk):
#     try:
#         category = Category.objects.get(pk=pk)
#     except Category.DoesNotExist:
#         raise NotFound  # raise가 실행 되면 이후는 실행 되지 않음
#
#     if request.method == "GET":
#         serializer = CategorySerializer(category)  # 카테고리 하나만 찾기 때문에 many= 필요 없음, DB에서 넘어오는 첫 번째 인스턴스 번역
#         return Response(serializer.data)
#
#     elif request.method == "PUT":
#         # DB에서 가져온 category와 사용자로부터 받은 data를 합쳐서 serializer를 만듦.
#         serializer = CategorySerializer(
#             category,
#             data=request.data, # 사용자로부터 오는 request.data는 완전하지 않을 수 있음
#             partial=True, # 이를 알려주는 것이 partial=
#         )
#         if serializer.is_valid():
#             updated_category = serializer.save() # 이 상황에서 .save()는 create()를 실행시키지 않음. update() 실행
#             return Response(CategorySerializer(updated_category).data)
#         else:
#             return Response(serializer.errors)
#
#     elif request.method == "DELETE":
#         category.delete()
#         return Response(status=HTTP_204_NO_CONTENT)

# ==================================== 3 djang rest framework 사용 방식 2 =======================================
from rest_framework.views import APIView

class Categories(APIView):
    def get(self, request):
        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)  # category 객체 여러개 many=
        return Response(serializer.data)
    def post(self, request): # 카테고리 만들기
        serializer = CategorySerializer(data=request.data)  # user가 보낸 데이터를 번역하려면 data= 사용
        if serializer.is_valid():
            new_category = serializer.save()  # save() 실행 하면 create() 메소드 실행
            return Response(CategorySerializer(new_category).data)
        else:
            return Response(serializers.errors)



class CategoryDetail(APIView): # APIView와 model의 이름이 겹치면 안 됨

    def get_object(self, pk): # 객체 하나 찾아오기
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound  # raise가 실행 되면 이후는 실행 되지 않음

    def get(self, request, pk):
        serializer = CategorySerializer(self.get_object(pk))  # 카테고리 하나만 찾기 때문에 many= 필요 없음, DB에서 넘어오는 첫 번째 인스턴스 번역
        return Response(serializer.data)

    def put(self, request, pk):
        # DB에서 가져온 category와 사용자로부터 받은 data를 합쳐서 serializer를 만듦.
        serializer = CategorySerializer(
            self.get_object(pk),
            data=request.data,  # 사용자로부터 오는 request.data는 완전하지 않을 수 있음
            partial=True,  # 이를 알려주는 것이 partial=
        )
        if serializer.is_valid():
            updated_category = serializer.save()  # 이 상황에서 .save()는 create()를 실행시키지 않음. update() 실행
            return Response(CategorySerializer(updated_category).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)


@api_view(["GET", "PUT", "DELETE"])
def category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        raise NotFound  # raise가 실행 되면 이후는 실행 되지 않음

    if request.method == "GET":
        serializer = CategorySerializer(category)  # 카테고리 하나만 찾기 때문에 many= 필요 없음, DB에서 넘어오는 첫 번째 인스턴스 번역
        return Response(serializer.data)

    elif request.method == "PUT":
        # DB에서 가져온 category와 사용자로부터 받은 data를 합쳐서 serializer를 만듦.
        serializer = CategorySerializer(
            category,
            data=request.data, # 사용자로부터 오는 request.data는 완전하지 않을 수 있음
            partial=True, # 이를 알려주는 것이 partial=
        )
        if serializer.is_valid():
            updated_category = serializer.save() # 이 상황에서 .save()는 create()를 실행시키지 않음. update() 실행
            return Response(CategorySerializer(updated_category).data)
        else:
            return Response(serializer.errors)

    elif request.method == "DELETE":
        category.delete()
        return Response(status=HTTP_204_NO_CONTENT)




# Create your views here.
