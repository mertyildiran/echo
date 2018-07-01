from django.db import models

class Echo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='echos', on_delete=models.CASCADE)
    latitude = models.IntegerField()
    longitude = models.IntegerField()
    hearts = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created_at',)
