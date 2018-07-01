from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from core.models import Echo
from core.serializers import EchoSerializer


@csrf_exempt
def echo_list(request):
    """
    List all echos, or create a new echo.
    """
    if request.method == 'GET':
        echos = Echo.objects.all()
        serializer = EchoSerializer(echos, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = EchoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def echo_detail(request, pk):
    """
    Retrieve, update or delete an echo.
    """
    try:
        echo = Echo.objects.get(pk=pk)
    except Echo.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = EchoSerializer(echo)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = EchoSerializer(echo, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        echo.delete()
        return HttpResponse(status=204)
