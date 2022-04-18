import datetime
import logging
import math

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, \
    ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveDestroyAPIView
from .serializers import ProfileSerializer, RegisterSerializer, ArticleSerializer,ProfileForArticleSerializer
from .models import Article, Subjects, ProfilePhoto, Likes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from api.service.tasks import debug_task
from api.service.permissions import IsArticleOwnerPermission, IsWriterPermission

Profile = get_user_model()


class RegisterView(CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request):
        profile = request.data
        serializer = self.serializer_class(data=profile)
        if not serializer.is_valid():
            return Response(serializer.errors)

        else:
            new_profile = Profile(
                username=profile.get("username"),
                email=profile.get("email"),
                password=make_password(profile.get("password")),
            )
        try:
            new_profile.save()
        except Exception as error:
            return Response({"error": f"Not saved!({error})"})

        token = Token.objects.create(user=new_profile)
        response = {
            "token": token.pk,
            "username": profile.username,
            "email": profile.email,
        }
        # logger.info(f"Create user {profile.email}")
        return Response(response)


class PrivateCabinet(RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'patch', 'delete']

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return self.request.user


class Tets(APIView):
    queryset = Profile.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request):
        debug_task.delay()
        return Response({"celery"})


class ArticleView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProfileForArticleSerializer
    def get serializer():
        pass
    # FILTERS
    def get_queryset(self):
        if self.request.user.is_author:
            return Article.objects.all()
        else:
            self.serializer_class = ArticleSerializer
            return Article.objects.filter(is_public=True)


class ArticlesCreateView(CreateAPIView):
    """Создание и список статей"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsWriterPermission)
    serializer_class = ArticleSerializer


class ArticlesUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """Страница редактирования статей"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsArticleOwnerPermission)
    serializer_class = ArticleSerializer
    http_method_names = ['get', 'patch', 'delete']

    def get_queryset(self):
        return Article.objects.filter(id=self.kwargs["pk"])



class LikeSenderView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        pass
        #profile = request.user?
