from rest_framework.serializers import ModelSerializer, ValidationError,CharField
from .models import Articles
from django.contrib.auth import get_user_model

import re

User = get_user_model()


class UserSerializer(ModelSerializer):
    """Сериализатор для регистрации новых пользователей"""
    password2 = CharField(label="Repeat your password!",style={"input_type": "password"},write_only=True)
    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "password2",
            "is_author"

        )

        extra_kwargs = {
            'password': {"style": {"input_type": "password"}, 'write_only': True},
        }

    def validate(self, data):
        password = data["password"].strip()
        password2 =data["password2"].strip()
        email = data["email"].strip()

        if len(email) == 0:
            raise ValidationError("Empty email!")
        if not re.fullmatch(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", email):
            raise ValidationError("Wrong email!")

        try:
            User.objects.get(email = email)
        except:
            pass
        else:
            raise ValidationError("This email already exists!")

        if not password2==password:
            raise ValidationError("Passwords not match!")
        if len(password) < 8:
            raise ValidationError("Password too short!")
        elif not re.search(r'\d', password):
            raise ValidationError("Must be at least one number")
        elif not re.search(r'[!@#$%^&*a-zA-Zа-яА-ЯёЁ]', password):
            raise ValidationError("Must be at least one char or letter")
        else:
            return data


class LoginSerializer(ModelSerializer):
    """Сериализатор для входа"""
    class Meta:
        model = User
        fields = ("email", "password")
        extra_kwargs = {
            'password': {"style": {"input_type": "password"}, 'write_only': True},
        }

    def validate(self, data):
        password = data["password"].strip()
        email = data["email"].strip()
        q = len(email)
        w= re.fullmatch(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", email)
        if len(email) == 0:
            raise ValidationError("Empty email!")
        if not re.fullmatch(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", email):
            raise ValidationError("Wrong email!")
        if len(password) < 8:
            raise ValidationError("Password too short!")
        elif not re.search(r'\d', password):
            raise ValidationError("Must be at least one number")
        elif not re.search(r'[!@#$%^&*a-zA-Zа-яА-ЯёЁ]', password):
            raise ValidationError("Must be at least one char or letter")
        else:
            return data


class CabinetSerializer(ModelSerializer):
    """Сериализатор для личного кабинета"""
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
    def validate(self, data):
        password = data["password"].strip()
        if len(password) < 8:
            raise ValidationError("Password too short!")
        elif not re.search(r'\d', password):
            raise ValidationError("Must be at least one number")
        elif not re.search(r'[!@#$%^&*a-zA-Zа-яА-ЯёЁ]', password):
            raise ValidationError("Must be at least one char or letter")
        else:
            return data


class ArticlesSerializer(ModelSerializer):
    class Meta:
        model = Articles
        fields = ("id", "article_title", "article_text", "user_id", "is_public")
        extra_kwargs = {
            "user_id": {"read_only": True},
            "id": {"read_only": True},
        }
