from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__", # __str__ 메소드로 값 보여주기.
        "payload",
    )
    list_filter = (
        "rating",
    )
# Register your models here.
