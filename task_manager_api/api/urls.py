from django.urls.conf import path
from rest_framework import routers
from .views import (
    DashboardViewSet,
    ListCreateSprintView,
    RetrieveUpdateDestroySprintView,
    TaskViewSet,
    ListCreateCommentView,
    RetrieveUpdateDestroyCommentView
)

router = routers.SimpleRouter()
router.register('tasks', TaskViewSet, basename='task')
router.register('dashboards', DashboardViewSet, basename='dashboard')

urlpatterns = [
    # Sprints
    path('sprints/<int:dashboard_id>/', ListCreateSprintView.as_view()),
    path('sprint/<int:pk>/', RetrieveUpdateDestroySprintView.as_view()),

    # Comments
    path('comments/<int:task_id>/', ListCreateCommentView.as_view()),
    path('comment/<int:pk>/', RetrieveUpdateDestroyCommentView.as_view()),
] + router.urls
