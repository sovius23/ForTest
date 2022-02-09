from django.urls import path
from .views import RegisterView, PublicArticlesView,UserCabinet,ArticlesCreateUpdateDestroyView,LoginView

urlpatterns = [

    path("register", RegisterView.as_view()),
    path("login", LoginView.as_view()),
    path("cabinet/<int:pk>", UserCabinet.as_view()),
    path("articles/public", PublicArticlesView.as_view()),
    path("articles/edit", ArticlesCreateUpdateDestroyView.as_view()),

]
