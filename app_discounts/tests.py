from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class DiscountViewTestCase(TestCase):
    """Тест страницы Скидок"""
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

    def test_discount_detail_view(self):
        response = self.client.get(reverse("appdiscount:sale"))
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.context_data, "discounts")