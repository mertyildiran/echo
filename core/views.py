from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import Echo, Notification
from core.serializers import EchoSerializer, UserSerializer, NotificationSerializer
from django.contrib.auth.models import User
from rest_framework import generics
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from rest_framework.permissions import AllowAny, IsAdminUser
from django.contrib.auth.hashers import PBKDF2SHA1PasswordHasher
from django.conf import settings

SALT = getattr(settings, "PASSWORD_SALT", "salt")


class EchoList(APIView):
    """
    List echos by filter, or create a new echo.
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
            echos = []

        serializer = EchoSerializer(echos, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        try:
            if not User.objects.get(token__key=self.request.META['HTTP_AUTHORIZATION']).id == self.request.POST.get('owner', None):
                return Response("You cannot send echos in the name of a different user.", status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response("Your API key is wrong or your records are corrupted.", status=status.HTTP_401_UNAUTHORIZED)
        serializer = EchoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class StaffOnlyEchoList(APIView):
    """
    List all echos, or create a new echo.
    """

    permission_classes = (IsAdminUser,)

    def get(self, request, format=None):
        echos = Echo.objects.all().order_by('created_at')
        serializer = EchoSerializer(echos, many=True)
        return Response(serializer.data)


class EchoDetail(APIView):
    """
    Retrieve, update or delete an echo.
    """

    def get_object(self, pk):
        try:
            return Echo.objects.get(pk=pk)
        except Echo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def check_owner(self, request, echo):
        try:
            if not User.objects.get(token__key=self.request.META['HTTP_AUTHORIZATION']).id == echo.owner.id:
                return False
        except User.DoesNotExist:
            return False  # If there is no user with that API key then it's an unauthorized operation by default
        return True

    def get(self, request, pk, format=None):
        echo = self.get_object(pk)
        serializer = EchoSerializer(echo)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        echo = self.get_object(pk)
        if not self.check_owner(request, echo):
            return Response("You cannot update echo details that are belong to other users.", status=status.HTTP_403_FORBIDDEN)
        serializer = EchoSerializer(echo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        echo = self.get_object(pk)
        if not self.check_owner(request, echo):
            return Response("You cannot delete echos that are belong to other users.", status=status.HTTP_403_FORBIDDEN)
        echo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StaffOnlyUserList(APIView):
    """
    List all users.
    """

    permission_classes = (IsAdminUser,)

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class Register(APIView):
    """
    Create a new user.
    """

    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    """
    Authenticate.
    """

    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        username = self.request.POST.get('username', None)
        email = self.request.POST.get('email', None)
        password = self.request.POST.get('password', None)
        if not all([username, email, password]):
            return Response("You have to supply 'username', 'email' and 'password' parameters.", status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username, password=PBKDF2SHA1PasswordHasher().encode(password, SALT))
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=email, password=PBKDF2SHA1PasswordHasher().encode(password, SALT))
            except User.DoesNotExist:
                return Response("Login failed because of wrong user credentials.", status=status.HTTP_401_UNAUTHORIZED)
        if user:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response("Unknown internal server error.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserDetail(APIView):
    """
    Retrieve, update or delete a user.
    """

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def check_owner(self, request, pk):
        try:
            if not User.objects.get(token__key=self.request.META['HTTP_AUTHORIZATION']).id == pk:
                return False
        except User.DoesNotExist:
            return False  # If there is no user with that API key then it's an unauthorized operation by default
        return True

    def get(self, request, pk, format=None):
        username = self.request.query_params.get('username', None)
        if not username:
            return Response("You have to supply 'username' parameter.", status=status.HTTP_400_BAD_REQUEST)
        try:
            if not User.objects.get(username=username).id == pk:
                return Response("It is not possible get user details by doing random shots without knowing the correct ['username', 'id'] combination.", status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response("That 'username' doesn't even exist.", status=status.HTTP_401_UNAUTHORIZED)
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        if not self.check_owner(request, pk):
            return Response("You cannot update the account details of other users.", status=status.HTTP_403_FORBIDDEN)
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if not self.check_owner(request, pk):
            return Response("You cannot delete the accounts of other users.", status=status.HTTP_403_FORBIDDEN)
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NotificationList(APIView):
    """
    Retrieve or insert notifications
    """

    def get(self, request, format=None):
        try:
            notifications = Notification.objects.filter(sender=User.objects.get(token__key=self.request.META['HTTP_AUTHORIZATION']).id).order_by('-created_at')
        except User.DoesNotExist:
            return Response("Your API key is wrong or your records are corrupted.", status=status.HTTP_401_UNAUTHORIZED)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        try:
            self.request.POST.set('sender', User.objects.get(token__key=self.request.META['HTTP_AUTHORIZATION']).id)
        except User.DoesNotExist:
            return Response("Your API key is wrong or your records are corrupted.", status=status.HTTP_401_UNAUTHORIZED)
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
