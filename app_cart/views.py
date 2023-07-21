from app_cart.cart import Cart, CartDB
from app_cart.forms import CartAddProductInShopForm, CouponApplyForm
from app_cart.services import ComparisonServicesMixin
from app_catalog.models import ProductInShop
from app_discounts.models import Coupon
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST


def add_in_comparison(request, product_id):
    """
    Функция добавляет в список сравнений продукт и возвращает обратно на страницу
    """
    comparison = ComparisonServicesMixin(request=request)
    comparison.add_to_in_comparison(product_id=product_id)
    return redirect("appcatalog:catalog")


def list_product_in_comparison(request):
    """
    Функция выводит список продуктов в списке сравнения
    """
    comparison = ComparisonServicesMixin(request=request)
    content = comparison.get_goods_to_in_comparison()
    return render(request, "shops/comparison.jinja2", {"content": content})


def remove_product_in_comparison(request, product_id):
    """
    Функция удаляет товар из списка сравнения и возвращает обратно в список сравнений
    """
    comparison = ComparisonServicesMixin(request=request)
    comparison.remove_from_comparison(product_id=product_id)
    return redirect("app_cart:comparison_list")


def cart_add(request, product_in_shop_id):
    """
    Функция добавления товара в корзину
    """
    if request.user.is_authenticated:
        cart = CartDB(request)
    else:
        cart = Cart(request)
    product_in_shop = get_object_or_404(ProductInShop, id=product_in_shop_id)
    if request.method == "POST":
        form = CartAddProductInShopForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(
                product_in_shop=product_in_shop,
                quantity=cd["quantity"],
                update_quantity=cd["update"],
            )
    else:
        cart.add(product_in_shop=product_in_shop, quantity=1, update_quantity=False)
    return redirect(request.META["HTTP_REFERER"])


def cart_remove(request, product_in_shop_id):
    """
    Функция удаления товара из корзины
    """
    if request.user.is_authenticated:
        cart = CartDB(request)
    else:
        cart = Cart(request)
    product_in_shop = get_object_or_404(ProductInShop, id=product_in_shop_id)
    cart.remove(product_in_shop)
    return redirect("app_cart:cart_detail")


def cart_detail(request):
    """
    Функция делального отображения товаров в корзине
    """
    form = {}
    if request.user.is_authenticated:
        cart = CartDB(request)
        for item in cart:
            form["update_quantity_form"] = CartAddProductInShopForm(
                initial={"quantity": item.quantity, "update": True}
            )
            form["coupon_apply_form"] = CouponApplyForm()
    else:
        cart = Cart(request)
        for item in cart:
            form["update_quantity_form"] = CartAddProductInShopForm(
                initial={"quantity": item["quantity"], "update": True}
            )
            form["coupon_apply_form"] = CouponApplyForm()
    context = {"cart": cart, "form": form}
    return render(request, "cart/cart.jinja2", context=context)


@require_POST
def coupon_apply(request):
    """Функция выполнение промокода"""
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data["code"]
        try:
            coupon = Coupon.objects.get(
                code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True
            )
            request.session["coupon_id"] = coupon.id
        except Coupon.DoesNotExist:
            request.session["coupon_id"] = None
    return redirect("app_cart:cart_detail")
