from django.urls import path
from .views import ReviewListView, ReviewCreateView

urlpatterns = [
    path('listings/<int:listing_pk>/reviews/', ReviewListView.as_view(), name='review-list'),
    path('listings/<int:listing_pk>/reviews/create/', ReviewCreateView.as_view(), name='review-create'),
]
