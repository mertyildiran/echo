from rest_framework import serializers
from core.models import Echo, Profile
from django.contrib.auth.models import User

class EchoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Echo
        owner = serializers.ReadOnlyField(source='owner.username')
        fields = ('id', 'created_at', 'owner', 'audio', 'latitude', 'longitude', 'hearts', 'is_active')


class UserSerializer(serializers.ModelSerializer):
    echos = serializers.PrimaryKeyRelatedField(many=True, queryset=Echo.objects.all())
    bio = serializers.CharField(source="profile.bio")
    picture = serializers.FileField(source="profile.picture")
    location = serializers.CharField(source="profile.picture")
    birth_date = serializers.DateField(source="profile.birth_date")
    gender = serializers.CharField(source="profile.gender")
    sexual_pref = serializers.CharField(source="profile.sexual_pref")
    instagram = serializers.CharField(source="profile.instagram")
    twitter = serializers.CharField(source="profile.twitter")
    snapchat = serializers.CharField(source="profile.snapchat")

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'picture', 'birth_date', 'gender', 'echos', 'sexual_pref', 'location', 'bio')

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = super(UserSerializer, self).create(validated_data)
        self.update_or_create_profile(user, profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        self.update_or_create_profile(instance, profile_data)
        return super(UserSerializer, self).update(instance, validated_data)

    def update_or_create_profile(self, user, profile_data):
        # This always creates a Profile if the User is missing one;
        # change the logic here if that's not right for your app
        Profile.objects.update_or_create(user=user, defaults=profile_data)
