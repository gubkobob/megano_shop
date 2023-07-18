from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from app_orders.models import Order

User = get_user_model()


class OrderCreateViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(
            username="usertest",
            email="testuser@test.ru",
            phone_number="1234567891",
            password="Test12345test",
        )
        cls.user = User.objects.create_user(**cls.credentials)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.login(**self.credentials)
        self.order = Order.objects.create(
            user=self.user,
            full_name='Test',
            phone_number="1234567891",
            email="test@test.ru",
            city="Test",
            address="addres_shop_1",
            delivery="Экспресс доставка",
            delivery_cost="500.00",
            payment="Онлайн со случайного чужого счета",
            comment="Test для заказа",
            status="Не оплачен",
            discount="0"
        )

    def tearDown(self) -> None:
        Order.objects.filter(pk=self.order.pk).delete()

    def test_create_order(self):
        self.assertTrue(Order.objects.filter(pk=self.order.pk).exists())

    def test_template_create_order(self):
        response = self.client.get(reverse("apporders:create_order"))
        self.assertContains(response, "Оформление заказа")

    def test_template_order_history(self):
        response = self.client.get(reverse("apporders:orders_history"))
        self.assertContains(response, "История заказов")
