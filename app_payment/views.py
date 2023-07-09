from django.shortcuts import redirect, render
from django.views.generic import ListView, TemplateView
from app_orders.models import Order
from django.contrib import messages
from app_payment.models import PayUserModel
from app_payment.tasks import logika



class PayView(ListView):
    model = PayUserModel
    template_name = 'app_payment/payment.jinja2'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = int(self.request.GET.get("order"))
        order_obj = Order.objects.get(id=order_id)
        context['orderitems'] = order_obj.items.first()
        context['order'] = order_obj
        return context



    def post(self, request):
        order_id = int(self.request.GET.get("order"))
        if request.method == "POST":
            numb = int("".join(request.POST.get("numero1").split(" ")))
            data1 = {'number': numb}
            response = logika.delay(order_id)
            context = {'message': "Необходимо дождаться очереди оплаты"}
            return redirect('/', context=context)






