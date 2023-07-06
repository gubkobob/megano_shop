from django.db import transaction
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View, CreateView
from decimal import Decimal

from app_cart.cart import CartDB
from app_users.models import User

from .services import reset_phone_format
from .models import OrderItem
from .forms import OrderForm


class CheckoutOrderView(View):

    def get(self, request, *args, **kwargs):
        # cart = CartDB(request)
        form = OrderForm(request.POST or None)
        context = {
            # 'cart': cart,
            'form': form
        }
        return render(request, 'app_orders/order_1.jinja2', context=context)


class CreateOrderView(CreateView):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = OrderForm(request.POST)
            cart = CartDB(request)
            user = User.objects.get(username=request.user.username)
            if form.is_valid():
                new_order = form.save(commit=False)
                new_order.full_name = form.cleaned_data['full_name']
                new_order.phone_number = form.cleaned_data['phone_number']
                new_order.email = form.cleaned_data['email']
                new_order.city = form.cleaned_data['city']
                new_order.address = form.cleaned_data['address']
                new_order.buying_type = form.cleaned_data['buying_type']
                new_order.payment = form.cleaned_data['payment']
                new_order.comment = form.cleaned_data['comment']
                new_order.status = form.cleaned_data['status']
                reset_phone_format(new_order)
                new_order.user = user
                new_order.save()
                for item in cart:
                    OrderItem.objects.create(order_id=new_order.id,
                                             product_in_shop=item.product_in_shop,
                                             price=item.price,
                                             quantity=item.quantity)
                new_order.save()
                user.orders.add(new_order)
                for item in cart:
                    cart.remove(product_in_shop=item.product_in_shop)

                order_items = OrderItem.objects.filter(order_id=new_order.id)

                get_total_price = sum(Decimal(item.price) * item.quantity for item in order_items)

                context = {
                    'form': new_order,
                    'order_items': order_items,
                    'get_total_price': get_total_price
                }

                return render(request, 'app_orders/order_2.jinja2', context=context)
                # return HttpResponseRedirect('/')
            return HttpResponseRedirect('/order/checkout/')
