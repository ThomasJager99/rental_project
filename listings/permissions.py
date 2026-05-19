from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsLandlord(BasePermission):
    message = 'Only landlords can perform this action'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'landlord'


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user
