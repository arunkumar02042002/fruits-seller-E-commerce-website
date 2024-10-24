from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import EmailValidatorSerializer, PasswordValidatorSerializer


class EmailValidatorApiView(GenericAPIView):
    serializer_class = EmailValidatorSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"status": "success", "message": "Email is valid.", "data": {}},
            status=status.HTTP_200_OK,
        )


class PasswordValidatorApiView(GenericAPIView):
    serializer_class = PasswordValidatorSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"status": "success", "message": "Password is valid.", "payload": {}},
            status=status.HTTP_200_OK,
        )
