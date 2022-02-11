from rest_framework.serializers import ValidationError
from django.http import Http404
from django.shortcuts import redirect
from rest_framework.response import Response

from .models import Articles
from .serializers import UserSerializer, ArticlesSerializer, LoginSerializer, CabinetSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, authenticate, get_user_model, logout
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from django.contrib.auth.hashers import make_password

User = get_user_model()


class RegisterView(CreateAPIView):
    """Панель регистрации"""

    serializer_class = UserSerializer

    def post(self, request):

        try:
            self.serializer_class.validate(self, data=request.data)
        except ValidationError as e:
            error = e.args[0]
            return Response({f"Error! {error}"})

        try:
            user = User.objects.create_user(
                request.data.get("email"),
                request.data.get("password"),
                request.data.get("is_author")
            )
        except Exception as e:
            return Response({"Error! Cannot save user!"})

        try:
            login(request, user)
        except Exception as e:
            return Response({"Error! Cannot sign in!"})
        else:
            return redirect("/api/cabinet")


class LoginView(APIView):
    """Панель входа"""

    serializer_class = LoginSerializer

    def post(self, request):

        try:
            self.serializer_class.validate(self, data=request.data)
        except ValidationError as e:
            error = e.args[0]
            return Response({f"Error! {error}"})

        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("/api/cabinet")
            else:
                return Response("Your account is not active!")
        else:
            return Response("Not Found!")


class LogOutView(APIView):
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        logout(request)
        return redirect("/api/articles/public")


class UserCabinetView(RetrieveUpdateDestroyAPIView):
    """Личный кабинет"""

    authentication_classes = (BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = CabinetSerializer
    queryset = User.objects.all()
    http_method_names = ['get', 'patch', 'delete']

    def get_object(self):
        return User.objects.get(id=self.request.user.id)

    def patch(self, request):
        try:
            request.data["password"] = make_password(request.data["password"])
            return super().patch(request)
        except:
            return super().patch(request)


class PublicArticlesView(ListAPIView):
    """Список публичных или всех статей(при регистрации)"""

    serializer_class = ArticlesSerializer

    def get_queryset(self):
        return Articles.objects.all() if self.request.user.is_authenticated else Articles.objects.filter(is_public=True)


class ArticlesListCreateView(ListCreateAPIView):
    """Создание и список статей"""
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = ArticlesSerializer

    def get_queryset(self):
        user = User.objects.get(id=self.request.user.id)
        return Articles.objects.filter(user_id=user)

    def post(self, request):
        article = Articles(
            user_id=User.objects.get(id=request.user.id),
            article_title=request.data.get("article_title"),
            article_text=request.data.get("article_text"),
            is_public=True if request.data.get("is_public") == "true" else False
        )
        try:
            article.save()
        except:
            return Response("Can`t save!")

        return redirect("/api/articles/create")


class ArticlesUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """Страница редактирования статей"""

    authentication_classes = (BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = ArticlesSerializer
    http_method_names = ['get', 'patch', 'delete']

    def get_object(self):
        try:
            article = Articles.objects.get(id=self.kwargs.get("pk"))
        except:
            raise Http404("Article not found")
        if article.user_id == User.objects.get(id=self.request.user.id):
            return article
        else:
            raise Http404("You don`t have rights!")

    def get_queryset(self):
        user = User.objects.get(id=self.request.user.id)
        return Articles.objects.filter(user_id=user)
