from rest_framework.serializers import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework.response import Response

from .models import User, Articles
from .serializers import UserSerializer, ArticlesSerializer, LoginSerializer, CabinetSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, authenticate
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from django.contrib.auth.hashers import make_password


class RegisterView(CreateAPIView):
    """Панель регистрации"""

    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            error = str(e.args[0]).split("\'")[3]
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
            return redirect(f"/api/cabinet/{user.id}")


class LoginView(APIView):
    """Панель входа"""

    serializer_class = LoginSerializer

    def post(self, request):

        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(f"/api/cabinet/{user.id}")
            else:
                return HttpResponse("Your account is not active!")
        else:
            return HttpResponse("Not Found!")


class UserCabinet(RetrieveUpdateDestroyAPIView):
    """Личный кабинет"""

    authentication_classes = (BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = CabinetSerializer
    queryset = User.objects.all()
    http_method_names = ['get', 'patch', 'delete']

    def get(self, request, pk):
        return super().get(request) if request.user.id == pk else HttpResponse("You don`t have permissions!")

    def patch(self, request, pk):
        if request.user.id == pk:
            user = User.objects.get(id=pk)

            if request.data.get("password"):
                user.password = make_password(request.data.get("password"))

            if request.data.get("is_author"):
                user.is_author = request.data.get("is_author")

            if request.data.get("is_subcscriber"):
                user.is_subscriber = True if request.data.get("is_subscriber") == "true" else False

            if request.data.get("is_alive"):
                user.is_alive = True if request.data.get("is_alive") == "true" else False

            try:
                user.save()
            except Exception as e:
                return Response({"Error! Cannot update user!"})

        else:
            return HttpResponse("You don`t have permissions!")

    def delete(self, request, pk):
        return super().delete(request) if request.user.id == pk else HttpResponse("You don`t have permissions!")


class PublicArticlesView(ListAPIView):
    """Список Статей"""

    serializer_class = ArticlesSerializer

    def get_queryset(self):
        return Articles.objects.all() if self.request.user.is_authenticated else Articles.objects.filter(is_public=True)


class ArticlesCreateUpdateDestroyView(ListCreateAPIView):
    """Страница редактирования статей"""

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
        article.save()
        return redirect(f"/api/articles/edit")

    def patch(self, request):
        article = Articles.objects.get(id=request.data.get("article_id"))
        if article.user_id == User.objects.get(
                id=request.user.get("id")
        ):
            if request.data.get("article_title"):
                article.article_title = request.data.get("article_title")
            if request.data.get("article_text"):
                article.article_text = request.data.get("article_text")
            if request.data.get("is_public"):
                article.is_public = True if request.data.get("is_public") == "true" else False
            try:
                article.save()
            except Exception as e:
                return Response({"Error! Cannot update an article!": e.error_list[0]})
        else:
            return HttpResponse("You don`t have permissions for this Article!")

    def delete(self, request):

        article = Articles.objects.get(id=request.data.get("article_id"))
        if article.user_id == User.objects.get(
                id=request.user.get("id")
        ):
            article.delete()

        return HttpResponse("You don`t have permissions for this Article!")
