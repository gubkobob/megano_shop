import time

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from app_payment.models import PayUserModel
from app_payment.tasks import logika


class PayView(ListView):
    model = PayUserModel
    template_name = 'app_payment/payment.jinja2'

    def post(self, request):
        data = int("".join(request.POST.get("numero1").split(" ")))
        data1 = {'number': data}

        logika.delay()

        return render(data1, 'app_payment/progressPayment.jinja2')

class PayView2(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'app_payment/progressPayment.jinja2'

    def get(self, request):
        queryset = PayUserModel.objects.all()
        return render(request, 'app_payment/progressPayment.jinja2')




