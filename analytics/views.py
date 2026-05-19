from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from .models import SearchHistory, ListingView
from listings.models import Listing
from listings.serializers import ListingSerializer


class MySearchHistoryView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # group search history by keyword and count occurrences
        history = SearchHistory.objects.filter(user=request.user)
        grouped = history.values('keyword').annotate(count=Count('keyword')).order_by('-count')[:20]
        return Response(list(grouped))


class PopularSearchesView(APIView):
    def get(self, request):
        popular = SearchHistory.objects.values('keyword').annotate(count=Count('keyword')).order_by('-count')[:10]
        return Response(list(popular))


class MyViewHistoryView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # get ids of listings the user has viewed
        viewed_ids = ListingView.objects.filter(user=request.user).values_list('listing_id', flat=True).distinct()[:20]
        listings = Listing.objects.filter(id__in=viewed_ids)
        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data)


class PopularListingsView(generics.ListAPIView):
    serializer_class = ListingSerializer

    def get_queryset(self):
        # order by views count to get most popular listings
        return Listing.objects.filter(is_active=True).order_by('-views_count')[:20]
