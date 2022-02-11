from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Articles
from django.contrib.auth import get_user_model
import re

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "is_author"
        )

        extra_kwargs = {
            'password': {"style": {"input_type": "password"}, 'write_only': True},
        }

    def validate(self, data):
        password = data["password"]
        if len(password) < 8:
            raise ValidationError("Password too short!")
        elif not re.search(r'\d', password):
            raise ValidationError("Must be at least one number")
        elif not re.search(r'[!@#$%^&*a-zA-Zа-яА-ЯёЁ]', password):
            raise ValidationError("Must be at least one char or letter")
        else:
            return data


class LoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")


class CabinetSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "is_author",
            "is_subscriber",
            "is_active"
        )

        extra_kwargs = {
            "password": {"style": {"input_type": "password"}, "write_only": True},
            "email": {"read_only": True}
        }


class ArticlesSerializer(ModelSerializer):
    class Meta:
        model = Articles
        fields = ("id", "article_title", "article_text", "user_id", "is_public")
        extra_kwargs = {
            "user_id": {"read_only": True},
            "id": {"read_only": True},
        }
