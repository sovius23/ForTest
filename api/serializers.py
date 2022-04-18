from .models import Article, Subjects
from rest_framework.serializers import ModelSerializer, StringRelatedField, SerializerMethodField
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from api.service import calculate_distance
Profile = get_user_model()


class ProfileSerializer(ModelSerializer):
    photos = StringRelatedField(many=True)
    class Meta:
        model = Profile
        fields = ('username', 'password', 'email','age','latitude','longitude','first_name','last_name','photos')

class RegisterSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ('username', 'password', 'email')
        extra_kwargs = {
            'password': {"style": {"input_type": "password"}, 'write_only': True},
        }
        
        
class PublicProfileForArticleSerializer(ModelSerializer):
    distance= SerializerMethodField()
    class Meta:
        model = Profile
        fields = ("username")
        
class AuthorProfileForArticleSerializer(ModelSerializer):
    distance= SerializerMethodField()
    class Meta:
        model = Profile
        fields = ("sex","age","last_seen","distance",'username')
    def get_distance(self, obj):
        profile = self.context.get("request").user
        q= calculate_distance.calculate_distance(profile.longitude,profile.latitude,obj.longitude,obj.latitude)
        return q

class ArticlesSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsSerializerMixin, self).__init__(*args, **kwargs)
        
    text = SerializerMethodField()
    profile = ProfileForArticleSerializer()
    class Meta:
        model = Article
        exclude = ["is_public"]
        def get_text(self,obj):
            if view.one:
                return obj.text
            else: return f"{obj.text[0:100]}..."
        
