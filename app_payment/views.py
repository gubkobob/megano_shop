from app_orders.models import Order
from app_payment.models import PayUserModel
from app_payment.tasks import logika
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView


class PayView(ListView):
    model = PayUserModel
    template_name = "app_payment/payment.jinja2"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        order_obj = Order.objects.get(id=int(self.kwargs.get("pk")))
        context["orderitems"] = order_obj.items.first()
        context["order"] = order_obj
        return context

    def post(self, request, pk=0):
        if request.method == "POST":
            logika.delay(pk)
            messages.add_message(
                request,
                messages.SUCCESS,
                "Оплата поставлена в очередь, статус оплаты можете посмотреть в Личном кабинете",
            )
            # context = {'message': "Необходимо дождаться очереди оплаты"}
            return redirect("/")
