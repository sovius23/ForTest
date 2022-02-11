from django.contrib.auth import get_user_model
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
        user.delete()

    def test_login_logout_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normallogin@user.com', password='foobar123')
        self.assertTrue(user.is_authenticated)
        self.client.logout()
        self.client.login(email='unnormal@user.com', password='foobar123')
        self.assertFalse(user.is_authenticated)
        self.client.login(email='normallogin@user.com',password='foobar123')
        self.assertTrue(user.is_authenticated)
        user.delete()

    def test_patch(self):
        User = get_user_model()
        user = User.objects.create_user(email='normalpatch@user.com', password='foobar123')
        response = self.client.patch('/api/cabinet', {'is_author': 'true', 'password': '12test12'})
        user.delete()