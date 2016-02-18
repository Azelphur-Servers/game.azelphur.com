from djangobb_forum.models import Post
from django.db.models.signals import post_save
import socket

SITE_URL = "https://game.azelphur.com"

def sendMsg(msg):
    s = socket.socket()
    s.connect(("localhost", 1079))
    s.send(msg)
    s.shutdown(socket.SHUT_WR)

def new_forum_post(sender, instance, created, **kwargs):
    if not created:
        return
    channel = "#azelphur"
    if instance.topic.forum.category.name == "Staff area":
        channel = "#staff"
    if instance.topic.post_count == 1:
        msg = "%s New forum topic: %s by %s in %s / %s %s%s\r\n" % (
            channel,
            instance.topic,
            instance.user,
            instance.topic.forum.category,
            instance.topic.forum,
            SITE_URL,
            instance.topic.get_absolute_url()
        )
    else:
        msg = "%s New forum post by %s in %s / %s - %s%s\r\n" % (
            channel,
            instance.user,
            instance.topic.forum.category,
            instance.topic,
            SITE_URL,
            instance.get_absolute_url()
        )
    sendMsg(msg)

post_save.connect(new_forum_post, sender=Post)
