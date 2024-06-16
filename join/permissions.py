from rest_framework import permissions


class IsBoardUser(permissions.BasePermission):
    """
    Custom permission that checks if the user is associated with the board.
    
    Methods:
        has_object_permission: Returns True if the user is in the list of users associated with the board.
    """
    def has_object_permission(self, request,obj):
        return request.user in obj.users.all