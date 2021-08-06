from django.urls.conf import path
from rest_framework import routers
from .views import (
    DashboardViewSet,
    CreateSprintView,
    RetrieveUpdateDestroySprintView,
    TaskViewSet,
    CreateCommentView,
    RetrieveUpdateDestroyCommentView
)

router = routers.SimpleRouter()
router.register('tasks', TaskViewSet, basename='task')
router.register('dashboards', DashboardViewSet, basename='dashboard')

urlpatterns = [
    # Sprints
    path('sprints/', CreateSprintView.as_view()),
    path('sprints/<int:pk>/', RetrieveUpdateDestroySprintView.as_view()),

    # Comments
    path('comments/', CreateCommentView.as_view()),
    path('comments/<int:pk>/', RetrieveUpdateDestroyCommentView.as_view()),
] + router.urls
