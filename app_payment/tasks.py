from time import sleep
import random

from celery import shared_task

from app_orders.models import Order


@shared_task
def logika(order_id: int):
    """Sends an email when the feedback form has been submitted."""
    order_obj = Order.objects.get(id=order_id)
    randBits = bool(random.choice([True, False]))
    sleep(5)
    if randBits:
        order_obj.status = 'Оплачен'
        order_obj.save()
        return {'status': True}
    return {'status': False}


