from django.db import models

from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    """Simple User"""
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': "A user with that email already exists."
        }
    )

    is_subscriber = models.BooleanField(default=True)
    is_author = models.BooleanField(default=False)
    sex = models.BooleanField(blank=True, null=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    last_seen = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.username


class ProfilePhoto(models.Model):
    profile = models.ForeignKey(Profile, related_name='photos', on_delete=models.CASCADE)
    photo = models.FileField(models.Model)


class Subjects(models.Model):
    """List of subjects"""
    subject = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Subjects'

    def __str__(self):
        return self.subject


class Article(models.Model):
    """Simple articles model"""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='user_articles')
    created = models.DateTimeField(auto_now_add=True)
    header = models.CharField(blank=True, max_length=255)
    text = models.TextField()
    likes = models.IntegerField(default=0)
    is_public = models.BooleanField(default=False)
    subjects = models.ManyToManyField(Subjects)

    class Meta:
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.header


class Likes(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='who_did_i_like')

    class Meta:
        verbose_name_plural = 'Likes'

    def __str__(self):
        return self.profile
