from django.db import transaction
from django.db.models import Sum, F
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View, CreateView, DetailView, ListView
from decimal import Decimal

from app_cart.cart import CartDB
from app_users.models import User
from app_administrator.models import SettingsModel
from app_catalog.models import ProductInShop

from .services import reset_phone_format
from .models import OrderItem, Order
from .forms import OrderForm


class CheckoutOrderView(View):

    def get(self, request, *args, **kwargs):
        # cart = CartDB(request)
        form = OrderForm(request.POST or None)
        settings_price = SettingsModel.objects.all()

        context = {
            # 'cart': cart,
            'form': form,
            'settings_price': settings_price
        }
        return render(request, 'app_orders/order_1.jinja2', context=context)


class CreateOrderView(CreateView):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = OrderForm(request.POST)
            cart = CartDB(request)
            product_in_shop = ProductInShop.objects.all()
            user = User.objects.get(username=request.user.username)
            if form.is_valid():
                new_order = form.save(commit=False)
                new_order.full_name = form.cleaned_data['full_name']
                new_order.phone_number = form.cleaned_data['phone_number']
                new_order.email = form.cleaned_data['email']
                new_order.city = form.cleaned_data['city']
                new_order.address = form.cleaned_data['address']
                new_order.delivery = form.cleaned_data['delivery']
                new_order.payment = form.cleaned_data['payment']
                new_order.comment = form.cleaned_data['comment']
                new_order.status = form.cleaned_data['status']
                reset_phone_format(new_order)
                new_order.user = user
                for item in cart:
                    if item.quantity > item.product_in_shop.quantity:
                        return HttpResponseRedirect('/cart/')
                    else:
                        new_order.save()
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


class OrderDetailView(DetailView):

    template_name = "app_orders/oneorder.jinja2"
    queryset = Order.objects.prefetch_related("items").annotate(avg_price=Sum(F("items__price") * F("items__quantity")))
    context_object_name = "order"


class OrdersListView(ListView):
    template_name = "app_orders/historyorder.jinja2"
    context_object_name = "orders"
    def get_queryset(self):
        queryset = Order.objects.filter(user_id=self.request.user.id).\
            annotate(avg_price=Sum(F("items__price") * F("items__quantity"))).\
            all()
        return queryset
