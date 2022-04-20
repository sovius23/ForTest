from django.contrib.auth import get_user_model
from django.db import models

Profile = get_user_model()

class Chat(models.Model):
    name= models.CharField(max_length=255,default="")
    users = models.ManyToManyField(Profile)

    def __str__(self):
        return self.name
# class OpenChats(models.Model):
#     user=models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name="open_chats",blank=True, null=True)
#     chat = models.ForeignKey(Chat, on_delete=models.DO_NOTHING, related_name="user2",blank=True, null=True)

class Messages(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    text = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name="messages")
    created = models.DateTimeField(auto_now_add=True)
