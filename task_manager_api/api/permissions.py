from rest_framework.permissions import BasePermission


class IsMemberOfDashboard(BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        class_name = obj.__class__.__name__.lower()
        has_permission = False
        user = request.user
        sprint = None

        if class_name == 'sprint':
            sprint = obj
        elif 'sprint' in obj:
            sprint = obj.sprint

        if sprint and user in sprint.dashboard.members.all():
            has_permission = True

        return has_permission
