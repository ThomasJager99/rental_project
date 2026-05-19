from django.db import models
from django.conf import settings


class Listing(models.Model):
    PROPERTY_TYPES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('studio', 'Studio'),
        ('room', 'Room'),
        ('other', 'Other'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rooms = models.PositiveIntegerField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, default='apartment')
    is_active = models.BooleanField(default=True)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
