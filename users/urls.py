from django.urls import path
from . import views

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("", views.Users.as_view()),
    # *********** 순서 주의
    # path("<str:username>", views.PublicUser.as_view()), # 이 url 때문에 /me를 username으로 받아들여 오류 발생
    path("me", views.Me.as_view()),
    path("change-password", views.ChangePassword.as_view()),
    # V1 쿠키 로그인
    path("log-in", views.LogIn.as_view()),
    path("log-out", views.LogOut.as_view()),
    path("@<str:username>", views.PublicUser.as_view()), # me 아래로 내리면 제대로 작동, me라는 user가 있을 수 있기 때문에 @ 추가

    path("@<str:username>/rooms", views.ShowRooms.as_view()),
    path("@<str:username>/reviews", views.ShowReviews.as_view()),

    # V2 auth token
    path("token-login", obtain_auth_token), # token을 얻기 위한 api username, pw를 보내면 token 반환
    # POST { "username" : "seheon", "password": 1234 } -> token 받음
    # GET headers에서 Authorization : Token -------------- 보내면 인증

    # V3 JWT
    path("jwt-login", views.JWTLogIn.as_view()),

    path("github", views.GithubLogIn.as_view()),
    path("kakao", views.KakaoLogIn.as_view()),
    path("naver", views.NaverLogIn.as_view()),

]