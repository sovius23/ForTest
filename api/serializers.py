from rest_framework.serializers import ModelSerializer
from .models import User, Articles


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password", "is_author")
        extra_kwargs = {'password': {'write_only': True}}


class LoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")

class ArticleAuthorSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "id")

class ArticlesSerializer(ModelSerializer):
    user_id = ArticleAuthorSerializer()

    class Meta:
        model = Articles
        fields = ("article_title", "article_text", "user_id")
