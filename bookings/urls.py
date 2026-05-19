from django.urls import path
from .views import (
    BookingCreateView, MyBookingsView, BookingCancelView,
    BookingConfirmView, BookingRejectView, IncomingBookingsView,
)

urlpatterns = [
    path('', BookingCreateView.as_view(), name='booking-create'),
    path('my/', MyBookingsView.as_view(), name='my-bookings'),
    path('incoming/', IncomingBookingsView.as_view(), name='incoming-bookings'),
    path('<int:pk>/cancel/', BookingCancelView.as_view(), name='booking-cancel'),
    path('<int:pk>/confirm/', BookingConfirmView.as_view(), name='booking-confirm'),
    path('<int:pk>/reject/', BookingRejectView.as_view(), name='booking-reject'),
]
