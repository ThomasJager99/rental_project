from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from .serializers import BookingSerializer, BookingCreateSerializer


class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # only tenants are allowed to create bookings
        if request.user.role != 'tenant':
            return Response({'detail': 'Only tenants can create bookings'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)


class MyBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(tenant=self.request.user)


class BookingCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, tenant=request.user)
        except Booking.DoesNotExist:
            return Response({'detail': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        # can only cancel if status is pending or confirmed
        if booking.status not in ['pending', 'confirmed']:
            return Response({'detail': 'Cannot cancel this booking'}, status=status.HTTP_400_BAD_REQUEST)
        booking.status = 'cancelled'
        booking.save()
        return Response({'detail': 'Booking cancelled', 'status': booking.status})


class BookingConfirmView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, listing__owner=request.user)
        except Booking.DoesNotExist:
            return Response({'detail': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        if booking.status != 'pending':
            return Response({'detail': 'Only pending bookings can be confirmed'}, status=status.HTTP_400_BAD_REQUEST)
        booking.status = 'confirmed'
        booking.save()
        return Response({'detail': 'Booking confirmed', 'status': booking.status})


class BookingRejectView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, listing__owner=request.user)
        except Booking.DoesNotExist:
            return Response({'detail': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        if booking.status != 'pending':
            return Response({'detail': 'Only pending bookings can be rejected'}, status=status.HTTP_400_BAD_REQUEST)
        booking.status = 'rejected'
        booking.save()
        return Response({'detail': 'Booking rejected', 'status': booking.status})


class IncomingBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # get all bookings for listings owned by the current user
        return Booking.objects.filter(listing__owner=self.request.user)
