from .cart import Cart, CartDB, change_products_in_cart_db_from_cart
from .services import ComparisonServicesMixin


def cart(request):
    """
    Функция добавления обьекта корзины в сессии джанго
    """
    if request.user.is_authenticated:
        cart_db = CartDB(request)
        cart = Cart(request)
        change_products_in_cart_db_from_cart(cart_db=cart_db, cart=cart)
        cart.clear()
        cart = cart_db
    else:
        cart = Cart(request)
    return {"cart": cart}


def comparison(request):
    """
    Функция добавления обьекта сравнения в сессии джанго
    """
    return {"comparison": ComparisonServicesMixin(request)}
