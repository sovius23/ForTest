from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class User(AbstractUser):
    """Основная модель для хранения пользователей"""
    username = None
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': "A user with that email already exists."
        }
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    is_subscriber = models.BooleanField(default=True)
    is_author = models.BooleanField(default=False)

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Articles(models.Model):
    """Основная модель для хранения статей"""
    user_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    article_title = models.CharField(default=None, null=True, max_length=255)
    article_text = models.TextField()
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.article_title