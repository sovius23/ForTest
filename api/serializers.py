from django.contrib.auth.hashers import make_password
from django.core.validators import EmailValidator

from .models import Article, Subjects
from rest_framework.serializers import ModelSerializer, StringRelatedField, SerializerMethodField, CharField, \
    ValidationError
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from api.service import calculate_distance
from chat.models import Chat
Profile = get_user_model()

class ChatSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields="__all__"

class ProfileSerializer(ModelSerializer):
    photos = StringRelatedField(many=True)
    distance = SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('username', 'password', 'email', 'age', 'latitude', 'longitude', 'first_name', 'last_name', 'photos','is_author',"distance")
        extra_kwargs = {'email': {'read_only': True},
                        'password': {'write_only': True}}

    def get_distance(self, obj):
        profile = self.context.get("request").user
        if obj.longitude and obj.latitude:
            q = calculate_distance.calculate_distance(profile.longitude, profile.latitude, obj.longitude, obj.latitude)
            return q
        else: return 0

    def update(self, obj, validated_data):
        try:
            validated_data['password'] = make_password(validated_data['password'])
        finally:
            return super(ProfileSerializer, self).update(obj, validated_data)

class RegisterSerializer(ModelSerializer):
    password2 = CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Profile
        fields = ('username','email', 'password', 'password2')
        extra_kwargs = {
            'password': {"style": {"input_type": "password"}},
            'password2': {"style": {"input_type": "password"}},
        }

    def validate(self, data):
        if data.get("password") != data.get("password2"):
            raise ValidationError(("Пароли не совпадают!"))

        return super(RegisterSerializer, self).validate(data)



class PublicProfileForArticleSerializer(ModelSerializer):
    distance = SerializerMethodField()

    class Meta:
        model = Profile
        fields = ("username")


class AuthorProfileForArticleSerializer(ModelSerializer):
    distance = SerializerMethodField()

    class Meta:
        model = Profile
        fields = ("sex", "age", "last_seen", "distance", 'username')

    def get_distance(self, obj):
        profile = self.context.get("request").user
        q = calculate_distance.calculate_distance(profile.longitude, profile.latitude, obj.longitude, obj.latitude)
        return q


class ArticlesSerializer(ModelSerializer):
    # def __init__(self, *args, **kwargs):
    #     # Don't pass the 'fields' arg up to the superclass
    #     fields = kwargs.pop('fields', None)
    #
    #     # Instantiate the superclass normally
    #     super(DynamicFieldsSerializerMixin, self).__init__(*args, **kwargs)

    text = SerializerMethodField()

    # profile = ProfileForArticleSerializer()
    class Meta:
        model = Article
        exclude = ["is_public"]

        def get_text(self, obj):
            # if view.one:
            #     return obj.text
            # else:
            return f"{obj.text[0:100]}..."

