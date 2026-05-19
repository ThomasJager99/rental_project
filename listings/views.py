from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Listing
from .serializers import ListingSerializer, ListingCreateSerializer
from .filters import ListingFilter
from .permissions import IsLandlord, IsOwnerOrReadOnly
from analytics.models import SearchHistory, ListingView


class ListingListView(generics.ListAPIView):
    serializer_class = ListingSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ListingFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at', 'views_count']
    ordering = ['-created_at']

    def get_queryset(self):
        # return only active listings
        return Listing.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        # save search keyword to history if user is logged in
        search_query = request.query_params.get('search')
        if search_query and request.user.is_authenticated:
            SearchHistory.objects.create(user=request.user, keyword=search_query)
        return super().list(request, *args, **kwargs)


class ListingCreateView(generics.CreateAPIView):
    serializer_class = ListingCreateSerializer
    permission_classes = [IsAuthenticated, IsLandlord]


class ListingDetailView(generics.RetrieveAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # increment view counter every time someone opens a listing
        instance.views_count += 1
        instance.save()
        if request.user.is_authenticated:
            ListingView.objects.create(user=request.user, listing=instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ListingUpdateView(generics.UpdateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingCreateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class ListingDeleteView(generics.DestroyAPIView):
    queryset = Listing.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'detail': 'Listing deleted'}, status=status.HTTP_204_NO_CONTENT)


class ListingToggleStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        # only the owner can toggle listing status
        try:
            listing = Listing.objects.get(pk=pk, owner=request.user)
        except Listing.DoesNotExist:
            return Response({'detail': 'Listing not found'}, status=status.HTTP_404_NOT_FOUND)

        if listing.is_active:
            listing.is_active = False
        else:
            listing.is_active = True
        listing.save()

        return Response({
            'detail': f'Status changed to {"active" if listing.is_active else "inactive"}',
            'is_active': listing.is_active,
        })


class MyListingsView(generics.ListAPIView):
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated, IsLandlord]

    def get_queryset(self):
        # return only listings that belong to the current user
        return Listing.objects.filter(owner=self.request.user)
