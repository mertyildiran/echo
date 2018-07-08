from django.contrib import admin
from core.models import Echo, Profile, Token


class ProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'picture', 'birth_date', 'gender', 'sexual_pref', 'bio', 'instagram', 'twitter', 'snapchat')
admin.site.register(Profile, ProfileAdmin)

class TokenAdmin(admin.ModelAdmin):
    fields = ('user', 'key')
admin.site.register(Token, TokenAdmin)

class EchoAdmin(admin.ModelAdmin):
    fields = ('owner', 'audio', 'location', 'hearts', 'is_active')
admin.site.register(Echo, EchoAdmin)
