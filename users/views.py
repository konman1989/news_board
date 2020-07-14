from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import CreateUserSerializer


class UserCreateView(CreateAPIView):
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        refresh = RefreshToken.for_user(instance)
        data = serializer.data
        data['token'] = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        headers = self.get_success_headers(data)
        return Response(data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
