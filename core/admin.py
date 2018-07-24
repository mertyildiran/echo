from django.contrib import admin
from core.models import Echo, Profile, Notification
from django.contrib.gis.db import models
from mapwidgets.widgets import GooglePointFieldWidget


class ProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'picture', 'birth_date', 'gender', 'sexual_pref', 'bio', 'instagram', 'twitter', 'snapchat', 'hearts')
admin.site.register(Profile, ProfileAdmin)

class EchoAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }
    fields = ('owner', 'audio', 'location', 'is_active', 'always_active')
admin.site.register(Echo, EchoAdmin)

class NotificationAdmin(admin.ModelAdmin):
    fields = ('sender', 'receiver', 'unread')
admin.site.register(Notification, NotificationAdmin)
