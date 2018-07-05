from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import Echo
from core.serializers import EchoSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import generics
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D


class EchoList(APIView):
    """
    List all echos, or create a new echo.
    """

    def get(self, request, format=None):
        latitude = self.request.query_params.get('latitude', None)
        longitude = self.request.query_params.get('longitude', None)
        distance = self.request.query_params.get('distance', None)
        only_active = self.request.query_params.get('only_active', None)
        gender = self.request.query_params.get('gender', None)
        sexual_pref = self.request.query_params.get('sexual_pref', None)
        if distance:
            distance = int(distance)*1000  # km to meters
        if latitude and longitude:
            ref_location = Point(float(latitude), float(longitude))
        target_gender, target_sexual_pref = analyze_sexual_pref(gender, sexual_pref)
        target_gender, target_sexual_pref = shorten(target_gender, target_sexual_pref)
        if all([latitude, longitude, distance, gender, sexual_pref]):
            echos = Echo.objects.filter(location__distance_lte=(ref_location, D(m=distance)),
                                        owner__profile__gender__in=target_gender,
                                        owner__profile__sexual_pref__in=target_sexual_pref,
                                        is_active=True).annotate(distance=Distance('location', ref_location)).order_by('distance')
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


def analyze_sexual_pref(gender, sexual_pref):
    if sexual_pref == 'Heterosexual':
        if gender == 'Male':
            return ['Female'], ['Heterosexual', 'Bisexual']
        elif gender == 'Female':
            return ['Male'], ['Heterosexual', 'Bisexual']
    elif sexual_pref == "Bisexual":
        return ['Male', 'Female'], ['Heterosexual', 'Bisexual', 'Homosexual']
    elif sexual_pref == 'Homosexual':
        if gender == 'Male':
            return ['Male'], ['Homosexual', 'Bisexual']
        elif gender == 'Female':
            return ['Female'], ['Homosexual', 'Bisexual']
    elif sexual_pref == 'Sapiosexual':
        if gender == 'Male':
            return ['Female'], ['Sapiosexual']
        elif gender == 'Female':
            return ['Male'], ['Sapiosexual']
    return ['Female'], ['Heterosexual', 'Bisexual']

def shorten(target_gender, target_sexual_pref):
    GENDER_CHOICES = {
        'M': 'Male',
        'F': 'Female'
    }
    SEXUAL_CHOICES = {
        'A': 'Heterosexual',
        'B': 'Bisexual',
        'C': 'Homosexual',
        'D': 'Sapiosexual'
    }
    target_gender = [k for k, v in GENDER_CHOICES.items() if v in target_gender]
    target_sexual_pref = [k for k, v in SEXUAL_CHOICES.items() if v in target_sexual_pref]
    return target_gender, target_sexual_pref
