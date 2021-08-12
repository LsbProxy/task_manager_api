from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import UserLoginSerializer, RegisterSerializer, UserLoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics, views, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response


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

        if not user:
            return Response({'error': 'User does not exist/invalid Email or Password.'}, status=status.HTTP_404_NOT_FOUND)

        user_serializer = UserLoginSerializer(user)
        response = {**user_serializer.data, 'tokens': self.get_token(user)}

        return Response(response, status=status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
