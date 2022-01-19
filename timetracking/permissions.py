from django.conf import settings
from rest_framework import permissions


class IsAuthorized(permissions.BasePermission):
    """
    Object-level permission to only allow creators of an object to edit it.
    """

    message = "You are not authorized to perform this action"

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
