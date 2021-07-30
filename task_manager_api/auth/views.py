from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from .serializers import UserLoginSerializer, RegisterSerializer, UserLoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics, views, status
from rest_framework_simplejwt.tokens import RefreshToken


class UserLoginView(views.APIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def post(self, request):
        user = authenticate(
            password=request.data['password'], email=request.data['email'])
        user_serializer = UserLoginSerializer(user)
        response = {**user_serializer.data, 'tokens': self.get_token(user)}

        return JsonResponse(response, status=status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
