from django.contrib import admin
from .models import Review

class Wordfilter(admin.SimpleListFilter):
    title = "Filter by words!" # 필터 제목

    parameter_name = "word" # 파라미터 이름

    def lookups(self, reqeust, model_admin): # [("url에 표시 되는 이름","패널에 뜨는 이름")]      ex) url : word = good
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "Awesome"),
        ]
                                # =queryset
    def queryset(self, request, reviews): # return할 queryset (리뷰들)
        # # print(self.value()) # url에 있는 parameter= 다음의 값
        word = self.value() # 모든 필터 조건을 취소하면 self.value()는 None임
        if word:
            return reviews.filter(payload__contains=word)
        else:
            reviews

class RatingFilter(admin.SimpleListFilter):
    title = "Filter by Rating!"  # 필터 제목

    parameter_name = "rating"  # 파라미터 이름

    def lookups(self, reqeust, model_admin):  # [("url에 표시 되는 이름","패널에 뜨는 이름")]      ex) url : potato = good
         return [
            ("good", "Good"),
            ("bad", "Bad"),
        ]
        # =queryset
    def queryset(self, request, reviews):  # return 할 queryset (리뷰들)
        rate = self.value()
        if rate == "good":
            return reviews.filter(rating__gte=3)
        elif rate == "bad":
            return reviews.filter(rating__lt=3)
        else:
            return reviews





@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__", # __str__ 메소드로 값 보여주기.
        "payload",
    )
    list_filter = (
        Wordfilter,
        RatingFilter,
        "rating",
        "user__is_host",
        "room__category",
        "room__pet_friendly",
    )



# Register your models here.
