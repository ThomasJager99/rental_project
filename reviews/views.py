from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer
from listings.models import Listing


class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Review.objects.filter(listing_id=self.kwargs['listing_pk']).select_related('user')


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['listing'] = generics.get_object_or_404(Listing, pk=self.kwargs['listing_pk'])
        return ctx

    def create(self, request, *args, **kwargs):
        if request.user.role != 'tenant':
            return Response({'detail': 'Only tenants can leave reviews'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)
