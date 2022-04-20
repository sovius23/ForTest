from django.urls import path
from .views import RegisterView,ArticleView,ArticlesCreateView,ArticlesUpdateDestroyView,PrivateCabinet,Tets
from rest_framework.authtoken import views
from .logic.authentications import UserTokenAuthentication
urlpatterns = [
    path("user/register", RegisterView.as_view()),
    path('user/login', UserTokenAuthentication.as_view()),
    path('user/cabinet', PrivateCabinet.as_view()),
    path('new_article', ArticlesCreateView.as_view()),
    path('article', ArticleView.as_view()),
    path('new_article/<int:pk>', ArticlesUpdateDestroyView.as_view()),
    path('test', Tets.as_view()),
]
