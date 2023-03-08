from django.urls import path, include
from . import views

urlpatterns = [
    # V1
    # path("", views.categories),
    # path("<int:pk>", views.category),
    # V2
    # path("", views.Categories.as_view()),
    # path("<int:pk>", views.CategoryDetail.as_view()),
    # V3
    path
    (
        "",
        views.CategoryViewSet.as_view(
            {
                'get': 'list',
                'post': 'create',
            }
        )
    ),
    path(
        "<int:pk>",
        views.CategoryViewSet.as_view(
            {
                'get': 'retrieve',
                'put': 'partial_update',
                'delete': 'destroy',
            }
        )
    ),
]

# ============== DefaultRouter() 사용 url ================
# from rest_framework.routers import DefaultRouter
#
# router = DefaultRouter()
# router.register(r'', views.CategoryViewSet, basename="category")
# urlpatterns = [
#     path('', include(router.urls))
# ]