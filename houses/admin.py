from django.contrib import admin
from .models import House

# 장고 문서 : https://docs.djangoproject.com/ko/4.1/ref/contrib/admin/

# admin.site.register(House) # 이 방식은 admin 패널 customize 불가함

@admin.register(House)
class HouseAdmin(admin.ModelAdmin):

    fields = ("name", "address", ("price_per_night", "pets_allowed"))
    list_display = ("name", "price_per_night", "address", "pets_allowed")
    list_filter = ("price_per_night", "pets_allowed")
    search_fields = ("address",)
    list_display_links = ("name", "address")
    list_editable = ("pets_allowed",)

# Register your models here.
