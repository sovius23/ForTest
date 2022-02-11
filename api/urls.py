from django.urls import path
from .views import RegisterView, PublicArticlesView,UserCabinetView,ArticlesUpdateDestroyView,LoginView,LogOutView,ArticlesListCreateView

urlpatterns = [

    path("register", RegisterView.as_view()),
    path("login", LoginView.as_view()),
    path("logout", LogOutView.as_view()),
    path("cabinet", UserCabinetView.as_view()),
    path("articles/public", PublicArticlesView.as_view()),
    path("articles/create", ArticlesListCreateView.as_view()),
    path("articles/edit/<int:pk>", ArticlesUpdateDestroyView.as_view()),

]
