from django.contrib.auth import get_user_model
from .models import Articles
from django.test import TestCase


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foobar123')
        self.assertEqual(user.email, 'normal@user.com')
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
        user = User.objects.create_user(email='normal@user.com', password='foobar123')
        self.assertFalse(user.is_author)
        user.delete()
        user = User.objects.create_user(email='normalauthor@user.com', password='foobar123', is_author="true")
        self.assertTrue(user.is_author)
        article = Articles(
            user_id=user,
            article_title="title",
            article_text="article text",
            is_public="true",
        )
        article.save()
        self.assertFalse(article.is_public)
        article.article_title = "new title"
        article.save()
        self.assertEqual(article.article_title,"new title")

