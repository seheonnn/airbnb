from rest_framework.views import APIView

from bookings.models import Booking
from bookings.serializers import CheckMyBookingSerializer
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

# api/v1/bookings
class GetMyBookings(APIView):
    def get(self, request):
        bookings = Booking.objects.filter(user=request.user)
        serializer = CheckMyBookingSerializer(bookings, many=True)
        return Response(serializer.data)



# api/v1/bookings/1
class RoomBookingDelete(APIView):
    def get_object(self, pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            raise NotFound
    # def delete(self, request, pk):
    #     booking = self.get_object(pk)
    #     # if booking.user != request.user and booking.room == room:
    #     if booking.user != request.user:
    #         raise PermissionDenied
    #     booking.delete()
    #     return Response(status=HTTP_204_NO_CONTENT)

    # not_canceled 변수를 이용하여 예약 삭제
    def post(self, request, pk):
        booking = self.get_object(pk)
        if booking.user != request.user or booking.room.owner != request.user:
            raise PermissionDenied
        serializer = CheckMyBookingSerializer(booking, data={"canceled":True}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=HTTP_200_OK)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)