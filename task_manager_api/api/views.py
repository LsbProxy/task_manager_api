from .permissions import IsAuthor, IsMemberOfDashboard
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .models import Comment, Sprint, Task
from .serializers import (
    DashboardSerializer,
    SprintSerializer,
    TaskSerializer,
    CommentSerializer
)
import datetime


class DashboardViewSet(viewsets.ModelViewSet):
    serializer_class = DashboardSerializer

    def get_queryset(self):
        return self.request.user.dashboard_set.all()

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]


class CreateSprintView(generics.CreateAPIView):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer
    permission_classes = [IsAdminUser, IsMemberOfDashboard]

    def create(self, request):
        data = JSONParser().parse(request)
        data['end_date'] = str(
            datetime.datetime.now() + datetime.timedelta(weeks=2))

        serializer = self.get_serializer(data=data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RetrieveUpdateDestroySprintView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer

    def get_permissions(self):
        permission_classes = [IsMemberOfDashboard]

        if self.request.method == 'GET':
            permission_classes.append(IsAuthenticated)
        else:
            permission_classes.append(IsAdminUser)

        return [permission() for permission in permission_classes]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated, IsMemberOfDashboard]

        if self.request.method == 'DELETE':
            permission_classes.append(IsAdminUser)

        return [permission() for permission in permission_classes]

    def create(self, request):
        data = JSONParser().parse(request)
        data['author'] = request.user.username

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CreateCommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def post(self, request):
        data = JSONParser().parse(request)
        data['author'] = request.user.username

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RetrieveUpdateDestroyCommentView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthor]
