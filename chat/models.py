from django.db import models
from api.models import Profile


class Chat(models.Model):
    host = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="chats")
    members = models.ManyToManyField(Profile, related_name="current_chats", blank=True)


class Messages(models.Model):
    room = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    text = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name="messages")
    created = models.DateTimeField(auto_now_add=True)
