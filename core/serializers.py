from rest_framework import serializers
from core.models import Echo, Profile, Notification
from django.contrib.auth.models import User
from django.contrib.auth.hashers import PBKDF2SHA1PasswordHasher
from django.conf import settings
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

SALT = getattr(settings, "PASSWORD_SALT", "salt")


class UserSerializer(serializers.ModelSerializer):
    echoes = serializers.PrimaryKeyRelatedField(many=True, queryset=Echo.objects.all())
    first_name = serializers.CharField()
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField()
    is_active = serializers.BooleanField(default=True)
    picture = serializers.FileField(source="profile.picture")
    birth_date = serializers.DateField(source="profile.birth_date")
    gender = serializers.CharField(source="profile.gender")
    sexual_pref = serializers.CharField(source="profile.sexual_pref")

    bio = serializers.CharField(source="profile.bio", required=False)
    instagram = serializers.CharField(source="profile.instagram", required=False)
    twitter = serializers.CharField(source="profile.twitter", required=False)
    snapchat = serializers.CharField(source="profile.snapchat", required=False)

    hearts = serializers.IntegerField(source="profile.hearts", required=False, read_only=True)

    age = serializers.ReadOnlyField(source="profile.age")

    key = serializers.CharField(source="auth_token.key", required=False, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password',
                    'groups', 'user_permissions', 'is_staff', 'is_active',
                    'is_superuser', 'last_login', 'date_joined', 'picture',
                    'birth_date', 'gender', 'echoes', 'sexual_pref', 'bio',
                    'instagram', 'twitter', 'snapchat', 'hearts', 'age', 'key')

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        validated_data['password'] = PBKDF2SHA1PasswordHasher().encode(validated_data['password'], SALT)
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


class EchoSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False, read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='owner', write_only=True)
    distance = serializers.ReadOnlyField()

    class Meta:
        model = Echo
        fields = ('id', 'created_at', 'owner', 'owner_id', 'audio', 'location', 'distance', 'is_active')


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'created_at', 'sender', 'receiver', 'unread')
