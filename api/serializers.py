from .models import Article, Subjects
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

Profile = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        extra_kwargs = {
            'password': {"style": {"input_type": "password"}, 'write_only': True},
        }


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('username', 'password', 'email')
        extra_kwargs = {
            'password': {"style": {"input_type": "password"}, 'write_only': True},
        }
