from django.db import models


class IRCChannel(models.Model):
    channel = models.CharField(max_length=64)
    channel_title = models.CharField(max_length=64)
    default = models.BooleanField()

    def __unicode__(self):
        return self.channel_title
