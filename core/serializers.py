from rest_framework import serializers
from core.models import Echo
from django.contrib.auth.models import User

class EchoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Echo
        owner = serializers.ReadOnlyField(source='owner.username')
        fields = ('id', 'created_at', 'owner', 'latitude', 'longitude', 'hearts', 'is_active')

class UserSerializer(serializers.ModelSerializer):
    echos = serializers.PrimaryKeyRelatedField(many=True, queryset=Echo.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'echos')
