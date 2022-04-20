from .models import Chat, Messages
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class MessageSerializer(ModelSerializer):
    created = SerializerMethodField()
    profile = SerializerMethodField()

    class Meta:
        model = Messages
        fields = ("text", "created", "profile")

    def get_created(self, obj):
        return obj.created.strftime("%Y-%m-%d %H:%M")
    def get_profile(self, obj):
        return obj.profile.username


class ChatSerializer(ModelSerializer):
    messages = MessageSerializer(many=True)

    class Meta:
        model = Chat
        fields = "__all__"
