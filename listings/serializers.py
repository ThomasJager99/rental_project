from rest_framework import serializers
from .models import Listing
from users.serializers import UserSerializer


class ListingSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = [
            'id', 'owner', 'title', 'description', 'location',
            'price', 'rooms', 'property_type', 'is_active',
            'views_count', 'average_rating', 'created_at', 'updated_at',
        ]
        read_only_fields = ['owner', 'views_count', 'created_at', 'updated_at']

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews.exists():
            return None
        total = 0
        for review in reviews:
            total += review.rating
        avg = total / reviews.count()
        return round(avg, 1)


class ListingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ['id', 'title', 'description', 'location', 'price', 'rooms', 'property_type', 'is_active']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
