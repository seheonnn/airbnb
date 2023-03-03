from django.db import models

class CommonModel(models.Model):

    """ Common Model Definition """

    created_at = models.DateTimeField(auto_now_add=True)  # object가 처음 생성 되었을 때 시간 저장
    updated_at = models.DateTimeField(auto_now=True)  # object가 저장될 때마다 시간 저장

    class Meta:
        abstract = True # DB에 따로 테이블 생성하지 않도록 추가

# Create your models here.
