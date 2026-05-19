from django.contrib import admin
from .models import Listing

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'price', 'rooms', 'property_type', 'is_active', 'views_count']
    list_filter = ['property_type', 'is_active']
    search_fields = ['title', 'location']
