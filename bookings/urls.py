from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.GetMyBookings.as_view()),
    path("<int:pk>", views.RoomBookingDelete.as_view()),
]
