from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission


class HavingAccess(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated or user.is_superuser
        )
    
