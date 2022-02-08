from django.urls import path
from .views import RegisterView, PublicArticlesView

urlpatterns = [

    path("register", RegisterView.as_view()),
    path("articles/public", PublicArticlesView.as_view()),
    path("articles/edit", PublicArticlesView.as_view()),

]
