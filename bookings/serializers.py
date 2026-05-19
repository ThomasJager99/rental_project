from rest_framework import serializers
from .models import Booking
from listings.serializers import ListingSerializer
from users.serializers import UserSerializer


class BookingSerializer(serializers.ModelSerializer):
    listing = ListingSerializer(read_only=True)
    tenant = UserSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'listing', 'tenant', 'start_date', 'end_date', 'status', 'created_at']


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'listing', 'start_date', 'end_date']

    def validate(self, data):
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError('Start date must be before end date')
        listing = data['listing']
        if not listing.is_active:
            raise serializers.ValidationError('Listing is not active')
        # Check for overlapping bookings
        overlapping = Booking.objects.filter(
            listing=listing,
            status__in=['pending', 'confirmed'],
            start_date__lt=data['end_date'],
            end_date__gt=data['start_date'],
        )
        if overlapping.exists():
            raise serializers.ValidationError('These dates are already booked')
        return data

    def create(self, validated_data):
        validated_data['tenant'] = self.context['request'].user
        return super().create(validated_data)
