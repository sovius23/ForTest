from django.urls import path
from .views import RegisterView
from rest_framework.authtoken import views
from service.authentications import UserTokenAuthentication
urlpatterns = [
    path("user/register", RegisterView.as_view()),
    path('user/login', UserTokenAuthentication.as_view()),

]
