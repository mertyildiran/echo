from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os.path
import uuid
from django.contrib.gis.db import models as geo_models

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
    bio = models.TextField(max_length=500, blank=True)
    picture = models.FileField(null=True, blank=True, upload_to=profile_directory)
    address = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    SEXUAL_CHOICES = (
        ('A', 'Heterosexual'),
        ('B', 'Bisexual'),
        ('C', 'Homosexual'),
        ('D', 'Sapiosexual')
    )
    sexual_pref = models.CharField(max_length=1, choices=SEXUAL_CHOICES)
    instagram = models.CharField(max_length=30, blank=True)
    twitter = models.CharField(max_length=30, blank=True)
    snapchat = models.CharField(max_length=30, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
