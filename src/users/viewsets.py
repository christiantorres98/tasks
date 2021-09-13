from django.utils.translation import ugettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserModelSerializer, UserSignUpSerializer, TokenModelSerializer


class UserSignUpAPIView(APIView):
    http_method_names = ['post']
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={status.HTTP_201_CREATED: UserModelSerializer()}, request_body=UserModelSerializer)
    def post(self, request, *args, **kwargs):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)


class LoginAPIView(ObtainAuthToken):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(responses={
        status.HTTP_200_OK: TokenModelSerializer()}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserModelSerializer(instance=user).data
        })


class LogoutAPIView(APIView):
    http_method_names = ['post']
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={status.HTTP_204_NO_CONTENT: ''})
    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
