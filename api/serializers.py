from rest_framework.serializers import ModelSerializer
from .models import User, Articles

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password","is_author")
        extra_kwargs = {'password': {'write_only': True}}


class ArticlesSerializer(ModelSerializer):
    class Meta:
        model = Articles
        fields = "__all__"
