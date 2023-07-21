from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class CartViewTestCase(TestCase):
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

    def setUp(self) -> None:
        self.client.login(**self.credentials)

    def test_cart_detail_view(self):
        response = self.client.get(reverse("app_cart:cart_detail"))
        self.assertContains(response, "cart")

    def test_cart_detail_view_not_autheticated(self):
        self.client.logout()
        response = self.client.get(reverse("app_cart:cart_detail"))
        self.assertContains(response, "cart")


class ComparisonViewTestCase(TestCase):
    """Тест списка сравнений"""

    fixtures = [
        'fixtures/1_Setting.json',
        'fixtures/2_User.json',
        'fixtures/3_Category.json',
        'fixtures/4_SubCategory.json',
        'fixtures/5_Shop.json',
        'fixtures/6_Product.json',
        'fixtures/7_ProductInShop.json',
        'fixtures/8_ProductInShopImage.json',
        'fixtures/9_Specifications.json',
        'fixtures/10_Subspecifications.json',
        'fixtures/11_Discount.json',
    ]

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

    def setUp(self) -> None:
        self.client.login(**self.credentials)

    def test_comparison_detail_view(self):
        response = self.client.get(reverse("app_cart:comparison_list"))
        self.assertEquals(response.context, None)
        response_comparison = self.client.get(reverse("app_cart:add_in_comparison", kwargs={'product_id': 14}))
        self.assertRedirects(response_comparison, '/catalog/')
        self.assertTrue(list(x for x in self.client.session.values()), 14)

    def test_comparison_detail_view_not_autheticated(self):
        self.client.logout()
        response = self.client.get(reverse("app_cart:comparison_list"))
        self.assertContains(response, "comparison")

