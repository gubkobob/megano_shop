from decimal import Decimal

from app_administrator.models import SettingsModel
from app_cart.cart import CartDB
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpRequest
from django.db import transaction
from django.db.models import F, Sum
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, View

from .forms import OrderForm
from .models import Order, OrderItem
from .services import reset_phone_format

User = get_user_model()


class CreateOrderView(View):
    """
    Класс по созданию заказа
    """
    count_shop = []
    template_name = "app_orders/order.jinja2"
    form_class = OrderForm

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Функция заполнения формы создания зхаказа
        """
        form = OrderForm(request.POST or None)
        settings_price = SettingsModel.objects.all()

        context = {
            "form": form,
            "settings_price": settings_price
        }

        return render(request, self.template_name, context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        """
       Функция создания в БД заказа
       """
        if request.method == "POST":
            form = OrderForm(request.POST)
            cart = CartDB(request)
            user = request.user
            if form.is_valid():
                new_order = form.save(commit=False)
                new_order.full_name = form.cleaned_data["full_name"]
                new_order.phone_number = form.cleaned_data["phone_number"]
                reset_phone_format(new_order)
                new_order.email = form.cleaned_data["email"]
                new_order.city = form.cleaned_data["city"]
                new_order.address = form.cleaned_data["address"]
                new_order.delivery = form.cleaned_data["delivery"]
                new_order.payment = form.cleaned_data["payment"]
                new_order.comment = form.cleaned_data["comment"]
                new_order.status = form.cleaned_data["status"]
                new_order.user = user
                new_order.save()
                if cart.coupon:
                    new_order.coupon = cart.coupon
                    new_order.discount = cart.coupon.discount

                for item in cart:
                    if not item.product_in_shop.shop in self.count_shop:
                        self.count_shop.append(item.product_in_shop.shop)

                    if item.price_discount:
                        OrderItem.objects.create(
                            order_id=new_order.id,
                            product_in_shop=item.product_in_shop,
                            price=item.price_discount - (item.price_discount * new_order.discount / 100),
                            quantity=item.quantity,
                        )
                    else:
                        OrderItem.objects.create(
                            order_id=new_order.id,
                            product_in_shop=item.product_in_shop,
                            price=item.price - (item.price * new_order.discount / 100),
                            quantity=item.quantity,
                        )

                    cart.remove(product_in_shop=item.product_in_shop)

                    new_order.save()

                order_items = OrderItem.objects.filter(order_id=new_order.id)

                get_total_price = sum(Decimal(item.price) * item.quantity for item in order_items)

                if new_order.delivery == "Экспресс доставка":
                    new_order.delivery_cost = getattr(SettingsModel.objects.first(), "price_express_delivery")
                elif (get_total_price < getattr(SettingsModel.objects.first(), "min_total_price_order")) or \
                        (len(self.count_shop) > 1):
                    new_order.delivery_cost = getattr(SettingsModel.objects.first(), "price_ordinary_delivery")

                new_order.save()
                return redirect(f"/payment/{new_order.id}")
            return render(request, self.template_name)


class OrderDetailView(DetailView):

    template_name = "app_orders/oneorder.jinja2"
    queryset = Order.objects.prefetch_related("items").annotate(
        avg_price=Sum(F("items__price") * F("items__quantity"))
    )
    context_object_name = "order"


class OrdersListView(ListView):
    template_name = "app_orders/historyorder.jinja2"
    context_object_name = "orders"

    def get_queryset(self):
        queryset = (
            Order.objects.filter(user_id=self.request.user.id)
            .annotate(avg_price=Sum(F("items__price") * F("items__quantity")))
            .all()
        )
        return queryset
