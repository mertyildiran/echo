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
        upper_lat = self.request.query_params.get('upper_lat', None)
        lower_lat = self.request.query_params.get('lower_lat', None)
        upper_long = self.request.query_params.get('upper_long', None)
        lower_long = self.request.query_params.get('lower_lat', None)
        only_active = self.request.query_params.get('only_active', None)
        if all([upper_lat, lower_lat, upper_long, lower_long]):
            echos = Echo.objects.filter(latitude__range=(lower_lat, upper_lat), longitude__range=(lower_long, upper_long), is_active=True).order_by('created_at')
        elif only_active:
            echos = Echo.objects.filter(is_active=True).order_by('created_at')
        else:
            echos = Echo.objects.all().order_by('created_at')
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


class UserList(APIView):
    """
    List all users, or create a new user.
    """

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
    Retrieve, update or delete a user.
    """

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
