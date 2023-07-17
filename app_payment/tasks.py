import random
from time import sleep

from app_orders.models import Order, OrderItem
from celery import shared_task


@shared_task
def logika(order_id: int):
    """Метод обработки заказа (вычетается из магазина кол-во купленного товара) и смена статуса Заказа
    (смена статуса Заказа выполняется рандомно)
    :param order_id: передаваемый параметр:
        order_id - Номер заказа
    :type obj: int
    :return:
        status: Статус оплаты (True/False)
    :rtype: dict    """
    order_items = OrderItem.objects.filter(order=order_id)
    for order_item in order_items:
        many_product_order = order_item.quantity
        pid = order_item.product_in_shop
        pid.quantity = pid.quantity - many_product_order
        pid.save()
        print(pid.quantity)
    randBits = bool(random.choice([False]))
    sleep(5)
    order_obj = Order.objects.get(id=order_id)
    if randBits:
        order_obj.status = "paid for"
        order_obj.save()
        return {"status": True}
    return {"status": False}
