from rest_framework.permissions import BasePermission


class IsMemberOfDashboard(BasePermission):

    def has_object_permission(self, request, _, obj):
        return request.user in obj.dashboard.members.all()


class IsAuthor(BasePermission):

    def has_object_permission(self, request, _, obj):
        return request.user == obj.author
