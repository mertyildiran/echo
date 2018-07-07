from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os.path
import uuid
from django.contrib.gis.db import models as geo_models
from rest_framework.authtoken.models import Token as DRF_Token

def echo_directory(instance, filename):
    path = "uploads/echo/"
    name, extension = os.path.splitext(filename)
    format = str(instance.owner.id) + '_' + str(uuid.uuid4()) + extension
    return os.path.join(path, format)

def profile_directory(instance, filename):
    path = "uploads/profile/"
    name, extension = os.path.splitext(filename)
    format = str(instance.user.id) + extension
    return os.path.join(path, format)

class Echo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='echos', on_delete=models.CASCADE)
    audio = models.FileField(null=False, blank=False, upload_to=echo_directory)
    location = geo_models.PointField(null=False, blank=False, srid=4326, verbose_name="Location")
    hearts = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created_at',)


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    picture = models.FileField(null=False, blank=False, upload_to=profile_directory)
    birth_date = models.DateField(null=False, blank=False, default="2018-01-01")
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, null=False, blank=False, choices=GENDER_CHOICES)
    SEXUAL_CHOICES = (
        ('A', 'Heterosexual'),
        ('B', 'Bisexual'),
        ('C', 'Homosexual'),
        ('D', 'Sapiosexual')
    )
    sexual_pref = models.CharField(max_length=1, null=False, blank=False, choices=SEXUAL_CHOICES)

    bio = models.TextField(max_length=500, null=True, blank=True)
    instagram = models.CharField(max_length=30, null=True, blank=True)
    twitter = models.CharField(max_length=30, null=True, blank=True)
    snapchat = models.CharField(max_length=30, null=True, blank=True)


class Token(models.Model):
    user = models.OneToOneField(User, related_name='token', on_delete=models.CASCADE)
    key = models.CharField(max_length=46, null=True, blank=True)

    def save(self, **kwargs):
        self.key = "Token " + DRF_Token.objects.create(user=User.objects.get(pk=self.user.id)).key
        super(Token, self).save()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
