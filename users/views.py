from django.contrib.auth import authenticate, login, logout

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, NotFound

from rooms.models import Room
from rooms.serializers import RoomListSerializer
from reviews.models import Review
from reviews.serializers import UserReviewSerializer
from . import serializers
from .models import User
from django.conf import settings

import jwt

# api/v1/users/me
class Me(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            new_user = serializer.save()
            serializer = serializers.PrivateUserSerializer(new_user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


# api/v1/users
class Users(APIView):
    def post(self, request): # ModelSerializer가 uniquness 보장해주기 때문에 pw에 대한 validation만 하면 됨
        password = request.data.get('password')
        if not password:
            raise ParseError
        serializer = serializers.PrivateUserSerializer(data=request.data) # 해당 serializer에는 pw 포함 X
        if serializer.is_valid():
            # user.password = password # 이렇게 하면 raw pw가 그대로 DB에 들어감
            user = serializer.save()
            user.set_password(password) # pw hash화
            user.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

# api/v1/users/@seheon
class PublicUser(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExsists:
            raise NotFound
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

# api/v1/users/change-password
class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise ParseError

# api/v1/users/log-in
class LogIn(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            raise ParseError
        user = authenticate(request, username=username, password=password) # username, password가 일치하면 user 객체 반환
        if user:
            login(request, user) # user 정보가 담긴 session 생성, 사용자에게 cookie를 보내줌
            return Response({"ok": "Welcome!"})
        else:
            return Response({"error": "wrong password"})


# api/v1/users/log-out
class LogOut(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'pk': 'bye!'})


# api/v1/users/@seheon/rooms
class ShowRooms(APIView):
    def get(self, request, username):
        rooms = Room.objects.filter(owner__username=username)
        if rooms:
            serializer = RoomListSerializer(rooms, many=True, context={'request': request})
            return Response(serializer.data)
        else:
            raise ParseError(f"{username} does not have any rooms.")

# api/v1/users/@seheon/reviews
class ShowReviews(APIView):
    def get(self, request, username):
        reviews = Review.objects.filter(user__username=username).order_by("-created_at")
        if reviews:
            serializer = UserReviewSerializer(reviews, many=True)
            return Response(serializer.data)
        else:
            raise ParseError(f"{username} does not have any reviews.")

# V3 JWT 암호화
class JWTLogIn(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            raise ParseError
        user = authenticate(request, username=username, password=password)  # username, password가 일치하면 user 객체 반환
        if user:
            token = jwt.encode({"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256") # JWT token 발급
            return Response({"token": token})
        else:
            return Response({"error": "wrong password"})

import requests
# api/v1/users/github
class GithubLogIn(APIView):
    def post(self, request):
        try:
            code = request.data.get('code')
            access_token = requests.post(f"https://github.com/login/oauth/access_token?code={code}"
                                         f"&client_id=8c7475533617f2962128"
                                         f"&client_secret={settings.GH_SECRET}",
                                         headers={"Accept":"application/json"},
                                         )
            access_token = access_token.json().get("access_token")
            user_data = requests.get("https://api.github.com/user", headers={"Authorization": f"Bearer {access_token}", "Accept": "application/json"},)
            user_data = user_data.json()

            user_emails = requests.get("https://api.github.com/user/emails", headers={"Authorization": f"Bearer {access_token}", "Accept": "application/json"},)
            user_emails = user_emails.json()
            try:
                user = User.objects.get(email=user_emails[0]["email"])
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=user_data.get('login'),
                    email=user_emails[0]['email'],
                    name=user_data.get('name'),
                    avatar=user_data.get('avatar_url')
                )
                user.set_unusable_password() # pw없이 GitHub로만 로그인 가능.
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)