from django.contrib.auth import get_user_model
from .models import Articles
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
import json


class UsersManagersTests(TestCase):

    def test_create_login_logout_user(self):
        response = self.client.get("/api/articles/public")
        self.assertEqual(response.status_code, 200)
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foobar123')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_authenticated)
        response = self.client.get("/api/logout")
        self.assertEqual(response.status_code, 401)
        response = self.client.post("/api/login", {"email": 'normal@user.com', "password": 'foobar123'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo")

    def test_articles(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foobar123',is_author = 'true')
        response = self.client.post("/api/login",
                                    {"email": 'normal@user.com', "password": 'foobar123'})
        self.assertTrue(user.is_author)
        response = self.client.post("/api/articles/create", {"article_title": 'title1', "article_text": 'big text'})
        self.assertEqual(response.status_code, 200)
        article = Articles.objects.get(id=1)
        self.assertEqual(article.article_title, 'title1')
        self.client.delete("/api/articles/edit/1")
        with self.assertRaises(ObjectDoesNotExist):
            article = Articles.objects.get(id=1)