from users.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

import jwt
from django.conf import settings

# V1
class TrustMeBroAuthentication(BaseAuthentication):
    def authenticate(self, request): # view 실행 전에 먼저 실행되는 authentication 구현해야 함. 해당 request에는 user 정보 없음
        username = request.headers.get("Trust-me") # user의 정보를 어떤식으로 받을지 정할 수 있음.
        if not username:
            return None
        try:
            user = User.objects.get(username=username)
            return (user, None) # user가 앞에 오는 튜플을 반환해야 함 -> 규칙 !!
        except User.DoesNotExist:
            raise AuthenticationFailed(f"No user {username}")

# V3 JWT 복호화
class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Jwt') # header에 있는 jwt 받아와서 복호화
        if not token:
            return None
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        pk = decoded.get('pk')
        if not pk:
            raise AuthenticationFailed("Invalid Token")
        try:
            user = User.objects.get(pk=pk)
            return (user, None)
        except User.DoesNotExist:
            raise AuthenticationFailed("User Not Found")
