
from django.urls import path
from .views import UserLoginView, RegisterView, UserView

from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('login/refresh/', TokenRefreshView.as_view()),
    path('users/', UserView.as_view()),
]
