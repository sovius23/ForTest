from .models import Article, Subjects
from rest_framework.serializers import ModelSerializer, StringRelatedField, SerializerMethodField
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from api.service import calculate_distance
Profile = get_user_model()


class ProfileForArticleSerializer(ModelSerializer):
    distance= SerializerMethodField()
    class Meta:
        model = Profile
        fields = ("sex","age","longitude","latitude","last_seen","distance")
        extra_kwargs = {
            'password': {"style": {"input_type": "password"}, 'write_only': True},
        }
        
    def get_distance(self, obj):
        profile = self.context.get("request").user
        q= calculate_distance.calculate_distance(profile.longitude,profile.latitude,obj.longitude,obj.latitude)
        return q

class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

class RegisterSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ('username', 'password', 'email')
        extra_kwargs = {
            'password': {"style": {"input_type": "password"}, 'write_only': True},
        }


class ManyArticlesSerializer(ModelSerializer):
    text = SerializerMethodField()
    profile = ProfileForArticleSerializer()
    class Meta:
        model = Article
        fields = "__all__"
        exclude = ["is_public"]
        def get_text(self,obj):
            return f"{obj.text[0:100]}..."
        #def get_field_names():
        
class ArticleSerializer(ModelSerializer):
    profile = ProfileForArticleSerializer()
    class Meta:
        model = Article
        exclude = ["is_public"]
