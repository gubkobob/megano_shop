from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from app_cart.models import CartRegisteredUser
from app_catalog.models import ProductInShop

User = get_user_model()
class CartViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.credentials = dict(username="test2",
                               email="ss2@dd.ru",
                               phone_number="+7(123)100-12-31",
                               password="aaaa88*AAAA",
                               )
        cls.user = User.objects.create_user(**cls.credentials)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.user.delete()

    def setUp(self) -> None:
        self.client.login(**self.credentials)


    def test_cart_detail_view(self):
        response = self.client.get(reverse("app_cart:cart_detail"))
        self.assertContains(response, "cart")

    def test_cart_detail_view_not_autheticated(self):
        self.client.logout()
        response = self.client.get(reverse("app_cart:cart_detail"))
        self.assertContains(response, "cart")



