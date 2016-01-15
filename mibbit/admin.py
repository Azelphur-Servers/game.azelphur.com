from mibbit.models import IRCChannel
from django.contrib import admin

class IRCChannelAdmin(admin.ModelAdmin):
    # ...
    list_display = ('channel', 'channel_title')

admin.site.register(IRCChannel, IRCChannelAdmin)
