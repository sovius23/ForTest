from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework.response import Response

from .models import User, Articles
from django.contrib.auth.hashers import make_password
from .serializers import UserSerializer, ArticlesSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication


class RegisterView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request):
        user = User(
            email=request.data.get("email"),
            password=make_password(request.data.get("password")),
            is_subscriber=True,
            is_author=True if request.data.get("is_author") == "true" else False
        )

        try:
            user.save()
        except Exception as e:
            return Response({"Error! Cannot register!": e.args[0]})
        else:

            try:
                login(request, user)
                q=5
            except Exception as e:
                return Response({"Error! Cannot sign in!": e.args[0]})
            else:
                return redirect("/api/articles/public")


class PublicArticlesView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ArticlesSerializer

    def get_queryset(self):
        return Articles.objects.all() if self.request.user.is_authenticated else Articles.objects.filter(is_public=True)


class ArticlesCreateUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ArticlesSerializer

    def post(self, request):
        if not self.request.user.is_author:
            return HttpResponse("You don`t have permissions! Become an author!")
        else:
            article = Articles(
                user_id=User.objects.get(id=request.user.get("id")),
                article_title=request.data.get("title"),
                article_text=request.data.get("text"),
                is_public=True if request.data.get("public") == "true" else False
            )

            try:
                article.save()
            except Exception as e:
                return Response({"Error! Cannot save an article!": e.args[0]})
            else:
                return HttpResponse("Created!")

    def patch(self, request,pk):
        if not self.request.user.is_author:
            return HttpResponse("You don`t have permissions! Become an author!")
        else:
            if Articles.objects.get(
                id=request.data.get("article_id")
            ).user_id == User.objects.get(
                id=request.user.get("id")
            ):
                article = Articles(
                    user_id=User.objects.get(id=request.user.get("id")),
                    article_title=request.data.get("title"),
                    article_text=request.data.get("text"),
                    is_public=True if request.data.get("public") == "true" else False
                )
            else:
                return HttpResponse("You don`t have permissions for this Article!")


