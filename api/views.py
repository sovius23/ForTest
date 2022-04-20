import datetime
import io
import logging
import math
from PIL import Image
import cv2
import numpy
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, \
    ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveDestroyAPIView
from .serializers import ProfileSerializer, RegisterSerializer, ArticlesSerializer, AuthorProfileForArticleSerializer
from .models import Article, Subjects, ProfilePhoto, Likes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from api.logic.tasks import mailing_list
from api.logic.permissions import IsArticleOwnerPermission, IsWriterPermission
from chat.models import Chat
from .service.add_watermark import image_changing
from chat.serializer import ChatSerializer
Profile = get_user_model()


class RegisterView(APIView):
    serializer_class = RegisterSerializer
    queryset = Profile.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        q= serializer.is_valid()
        e=serializer.errors
        if not serializer.is_valid():
            return Response(serializer.errors)

        else:
            new_profile = Profile.objects.create_user(
                request.data.get("username"),
                request.data.get("email"),
                request.data.get("password"),
            )

            token = Token.objects.create(user=new_profile)
            response = {
                "token": token.pk,
                "username": request.data.get("username"),
                "email": request.data.get("email"),
            }
        # logger.info(f"Create user {profile.email}")
        return Response(response)


class PrivateCabinet(RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'patch', 'delete']

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return self.request.user


class Tets(ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    # def post(self, request):
    #     # debug_task.delay()
    #     image_changing(request.data, request.user)
    #     return Response({"celery"})


class ArticleView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AuthorProfileForArticleSerializer

    # def get_serializer(self,request):
    #     pass
    # FILTERS
    def get_queryset(self):
        if self.request.user.is_author:
            return Article.objects.all()
        else:
            self.serializer_class = ArticlesSerializer
            return Article.objects.filter(is_public=True)


class ArticlesCreateView(CreateAPIView):
    """Создание и список статей"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsWriterPermission)
    serializer_class = ArticlesSerializer


class ArticlesUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """Страница редактирования статей"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsArticleOwnerPermission)
    serializer_class = ArticlesSerializer
    http_method_names = ['get', 'patch', 'delete']

    def get_queryset(self):
        return Article.objects.filter(id=self.kwargs["pk"])


class LikeSenderView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        pass
        # profile = request.user?
