from .permissions import IsMemberOfDashboard
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .models import Comment, Sprint, Task
from .serializers import (
    CreateTaskSerializer,
    CreateUpdateDashboardSerializer,
    DashboardSerializer,
    ListCreateSprintSerializer,
    RetrieveUpdateDestroySprintSerializer,
    TaskSerializer,
    CommentSerializer
)
import datetime


class DashboardViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return self.request.user.dashboard_set.all()

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateUpdateDashboardSerializer

        return DashboardSerializer

    def perform_create(self, serializer):
        self.update_dashboard_members(serializer)
        serializer.save()

    def perform_update(self, serializer):
        self.update_dashboard_members(serializer)
        serializer.save()

    def update_dashboard_members(self, serializer):
        data = serializer.validated_data

        if 'members' in data and data['members']:
            user_list = []
            for username in data['members']:
                user = User.objects.get(username=username)
                if user:
                    user_list.append(user)
            data['members'] = user_list


class ListCreateSprintView(generics.ListCreateAPIView):
    serializer_class = ListCreateSprintSerializer

    def get_queryset(self):
        dashboard_id = self.kwargs.get('dashboard_id')
        dashboard = self.request.user.dashboard_set.get(id=dashboard_id)
        return dashboard.sprint_set.all()

    def create(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        data['dashboard'] = kwargs.get('dashboard_id')
        data['end_date'] = str(datetime.datetime.now() +
                               datetime.timedelta(weeks=2))

        serializer = self.get_serializer(data=data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RetrieveUpdateDestroySprintView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sprint.objects.all()
    serializer_class = RetrieveUpdateDestroySprintSerializer

    def get_permissions(self):
        permission_classes = [IsMemberOfDashboard]

        if self.request.method == 'GET':
            permission_classes.append(IsAuthenticated)
        else:
            permission_classes.append(IsAdminUser)

        return [permission() for permission in permission_classes]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateTaskSerializer
        else:
            return TaskSerializer

    def create(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        data['author'] = request.user.id
        data['assigned_to'] = None

        if data['assigned_to']:
            assigned_to = User.objects.get(username=data['assigned_to'])

            if assigned_to:
                data['assigned_to'] = assigned_to.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ListCreateCommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        task = get_object_or_404(Task, pk=self.kwargs['task_id'])
        return task.comment_set.all()

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        data['author'] = request.user.id
        data['task'] = Task.objects.get(pk=kwargs.get('task_id')).id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RetrieveUpdateDestroyCommentView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
