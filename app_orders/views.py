from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.views.generic import View
from django.contrib import messages

from app_cart.cart import Cart
from app_users.models import User
from app_catalog.models import ProductInShop

from .models import Order
from .forms import OrderForm


class CheckoutOrderView(View):

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        form = OrderForm(request.POST or None)
        context = {
            'cart': cart,
            'form': form
        }
        return render(request, 'app_orders/order_test.jinja2', context)


class CreateOrderView(View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        print('1')
        if request.method == 'POST':
            form = OrderForm(request.POST)
            print('3')
            if form.is_valid():
                print('form valid')
                new_order = form.save()
                new_order.full_name = form.cleaned_data['full_name']
                new_order.phone_number = form.cleaned_data['phone_number']
                new_order.email = form.cleaned_data['email']
                new_order.city = form.cleaned_data['city']
                new_order.address = form.cleaned_data['address']
                new_order.buying_type = form.cleaned_data['buying_type']
                new_order.payment = form.cleaned_data['payment']
                new_order.comment = form.cleaned_data['comment']
                print('5')
                new_order.save()
                print('6')
                Cart(request).clear()
                new_order.save()
                messages.add_message(request, messages.INFO, "Заказ оформлен. Корзина пуста.")
                return HttpResponseRedirect('/')
            print('form NOT valid')
            return HttpResponseRedirect('/order/checkout/')



