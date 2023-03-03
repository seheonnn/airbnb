from django.db import models
from django.contrib.auth.models import AbstractUser # 장고의 user를 import

# 아래 방식은 장고의 user를 상속받지 않고 처음부터 user를 만든다는 얘기임.
# class User(models.Model):
#     pass

# 장고의 user를 상속받는 user
class User(AbstractUser):
    first_name = models.CharField(max_length=150, editable=False) # editable=False -> 사용 X
    last_name = models.CharField(max_length=150, editable=False)
    name = models.CharField(max_length=150, default="")
    is_host = models.BooleanField(default=False) # 역할, 방을 빌려주는 사람인지, 빌리는 사람인지, BooleanField는 non-nullable field임

# Create your models here.
