from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import Echo
from core.serializers import EchoSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import generics


class EchoList(APIView):
    """
    List all echos, or create a new echo.
    """

    def get(self, request, format=None):
        echos = Echo.objects.all()
        serializer = EchoSerializer(echos, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EchoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class EchoDetail(APIView):
    """
    Retrieve, update or delete an echo.
    """

    def get_object(self, pk):
        try:
            return Echo.objects.get(pk=pk)
        except Echo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        echo = self.get_object(pk)
        serializer = EchoSerializer(echo)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        echo = self.get_object(pk)
        serializer = EchoSerializer(echo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        echo = self.get_object(pk)
        echo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
