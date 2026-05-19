from rest_framework import serializers
from .models import Review
from users.serializers import UserSerializer
from bookings.models import Booking


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'text', 'created_at']


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'text']

    def validate(self, data):
        request = self.context['request']
        listing = self.context['listing']
        # Review is only allowed after a confirmed booking
        has_booking = Booking.objects.filter(
            tenant=request.user,
            listing=listing,
            status='confirmed',
        ).exists()
        if not has_booking:
            raise serializers.ValidationError('You can only review a listing after a confirmed booking')
        if Review.objects.filter(user=request.user, listing=listing).exists():
            raise serializers.ValidationError('You have already reviewed this listing')
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['listing'] = self.context['listing']
        return super().create(validated_data)
