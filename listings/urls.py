from django.urls import path
from .views import (
    ListingListView, ListingCreateView, ListingDetailView,
    ListingUpdateView, ListingDeleteView, ListingToggleStatusView, MyListingsView,
)

urlpatterns = [
    path('', ListingListView.as_view(), name='listing-list'),
    path('create/', ListingCreateView.as_view(), name='listing-create'),
    path('my/', MyListingsView.as_view(), name='my-listings'),
    path('<int:pk>/', ListingDetailView.as_view(), name='listing-detail'),
    path('<int:pk>/update/', ListingUpdateView.as_view(), name='listing-update'),
    path('<int:pk>/delete/', ListingDeleteView.as_view(), name='listing-delete'),
    path('<int:pk>/toggle-status/', ListingToggleStatusView.as_view(), name='listing-toggle-status'),
]
