from django.urls import path
from .views import MySearchHistoryView, PopularSearchesView, MyViewHistoryView, PopularListingsView

urlpatterns = [
    path('search-history/', MySearchHistoryView.as_view(), name='search-history'),
    path('popular-searches/', PopularSearchesView.as_view(), name='popular-searches'),
    path('view-history/', MyViewHistoryView.as_view(), name='view-history'),
    path('popular-listings/', PopularListingsView.as_view(), name='popular-listings'),
]
