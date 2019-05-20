from rest_framework import permissions



class IsStaff(permissions.IsAuthenticated):
    """
    Require staff status.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return False
