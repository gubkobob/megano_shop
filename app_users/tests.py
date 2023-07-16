from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class RigisterViewTestCase(TestCase):
    def test_register_user_correct(self):
        response = self.client.post(
            reverse("app_users:register"),
            {
                "username": "test",
                "email": "ss@dd.ru",
                "phone_number": "+7(123)123-12-31",
                "password1": "aaaa88*AAAA",
                "password2": "aaaa88*AAAA",
            },
        )
        self.assertRedirects(response, reverse("app_users:profile"))
        self.assertTrue(User.objects.filter(email="ss@dd.ru").exists())

    def test_register_user_incorrect(self):
        response = self.client.post(
            reverse("app_users:register"),
            {
                "username": "test1",
                "email": "ss1@dd.ru",
                "phone_number": "+7(123)188-12-31",
                "password1": "qwerty",
                "password2": "qwerty",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email="ss1@dd.ru").exists())


class MyLoginViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.credentials = dict(
            username="test2",
            email="ss2@dd.ru",
            phone_number="+7(123)100-12-31",
            password="aaaa88*AAAA",
        )
        cls.user = User.objects.create_user(**cls.credentials)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.user.delete()

    def test_login_user_correct(self):
        response = self.client.post(
            reverse("app_users:login"),
            {
                "username": "ss2@dd.ru",
                "password": "aaaa88*AAAA",
            },
        )
        self.assertRedirects(response, reverse("app_users:profile"))


class ProfileAndAccountViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.credentials = dict(
            username="test",
            email="ss@dd.ru",
            phone_number="+7(123)100-12-31",
            password="aaaa88*AAAA",
        )
        cls.user = User.objects.create_user(**cls.credentials)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.user.delete()

    def setUp(self) -> None:
        self.client.login(username="ss@dd.ru", password="aaaa88*AAAA")
        self.user = User.objects.filter(email="ss@dd.ru").first()

    def test_user_profile(self):
        response = self.client.get(reverse("app_users:profile"))
        self.assertContains(response, self.user.email)
        self.assertEqual(response.status_code, 200)

    def test_user_account(self):
        response = self.client.get(reverse("app_users:account"))
        self.assertContains(response, self.user.username)
        self.assertEqual(response.status_code, 200)
