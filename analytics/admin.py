from django.contrib import admin
from .models import SearchHistory, ListingView

@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'keyword', 'created_at']

@admin.register(ListingView)
class ListingViewAdmin(admin.ModelAdmin):
    list_display = ['user', 'listing', 'viewed_at']
