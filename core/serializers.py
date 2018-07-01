from rest_framework import serializers
from core.models import Echo

class EchoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Echo
        fields = ('id', 'created_at', 'latitude', 'longitude', 'hearts', 'is_active')
