from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from chat.models import Messages, Chat
from django.contrib.auth import get_user_model
from .serializer import ChatSerializer

Profile = get_user_model()


class ChatConsumer(WebsocketConsumer):
    chat = None

    def connect(self):
        self.accept()
        target_user = Profile.objects.get(id=int(self.scope['url_route']['kwargs']['id']))
        user = self.scope.get("user")
        if Chat.objects.filter(users=target_user).get(users=user):
            self.chat = Chat.objects.filter(users=target_user).get(users=user)
            chat = ChatSerializer(self.chat, many=True).child.data.get(
                "messages")
            for message in chat:
                message_json = {
                    'event': "Send",
                    'message': message.get("text"),
                    'send': message.get("created"),
                    'by': message.get("profile"),
                }
                self.send(text_data=json.dumps(message_json))
        else:
            new_chat = Chat(
                name=f"{user.username}+{target_user.username}"
            )
            new_chat.users.add(target_user)
            new_chat.users.add(user)
            self.chat = new_chat

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        new_message = Messages(
            chat=self.chat,
            text=text_data,
            profile=self.scope.get("user"),
        )
        new_message.save()
        e=new_message
        self.send(text_data=json.dumps(
            {
                'event': "Send",
                'message': new_message.text,
                'send': new_message.created.strftime("%Y-%m-%d %H:%M"),
                'by': new_message.profile.username,
            }
        ))

    def chat_message(self, event):
        message = event['message']
        # username = event['username']
        for i in Messages.objects.all():
            self.send(text_data=json.dumps({
                'event': "Send",
                'message': i.text,
                # 'username': username
            }))
