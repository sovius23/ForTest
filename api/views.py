from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework.response import Response

from .models import User, Articles
from .serializers import UserSerializer, ArticlesSerializer, LoginSerializer
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
        user = User.objects.create_user(
            request.data.get("email"),
            request.data.get("password"),
            request.data.get("is_author")
        )

        try:
            login(request, user)
        except Exception as e:
            return Response({"Error! Cannot sign in!": e.error_list[0]})
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
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ['get', 'patch', 'delete']

    def get(self, request, pk):
        return super().get(request) if request.user.id == pk else HttpResponse("You don`t have permissions!")

    def patch(self, request, pk):
        request.data["password"] = make_password(request.data.get("password"))
        return super().patch(request) if request.user.id == pk else HttpResponse("You don`t have permissions!")

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
        if not self.request.user.is_author:
            return HttpResponse("You don`t have permissions! Become an author!")
        else:
            article = Articles(
                user_id=User.objects.get(id=request.user.id),
                article_title=request.data.get("article_title"),
                article_text=request.data.get("article_text"),
                is_public=True if request.data.get("public") == "true" else False
            )

            try:
                article.save()
            except Exception as e:
                return Response({"Error! Cannot save an article!": e.error_list[0]})
            else:
                return HttpResponse("Created!")

    def patch(self, request):
        article = Articles.objects.get(id=request.data.get("article_id"))
        if article.user_id == User.objects.get(
                id=request.user.get("id")
        ):
            article = Articles(
                user_id=User.objects.get(id=request.user.get("id")),
                article_title=request.data.get("title"),
                article_text=request.data.get("text"),
                is_public=True if request.data.get("public") == "true" else False
            )
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
