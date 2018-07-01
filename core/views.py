from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Echo
from core.serializers import EchoSerializer


@api_view(['GET', 'POST'])
def echo_list(request, format=None):
    """
    List all echos, or create a new echo.
    """
    if request.method == 'GET':
        echos = Echo.objects.all()
        serializer = EchoSerializer(echos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EchoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def echo_detail(request, pk, format=None):
    """
    Retrieve, update or delete an echo.
    """
    try:
        echo = Echo.objects.get(pk=pk)
    except Echo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EchoSerializer(echo)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EchoSerializer(echo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        echo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
