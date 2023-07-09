from .cart import Cart, CartDB, change_products_in_cart_db_from_cart
from .services import ComparisonServicesMixin


def cart(request):
    if request.user.is_authenticated:
        cart_db = CartDB(request)
        cart = Cart(request)
        change_products_in_cart_db_from_cart(cart_db=cart_db, cart=cart)
        cart.clear()
        cart = cart_db
    else:
        cart = Cart(request)
    return {'cart': cart}


def comparison(request):
    return {'comparison': ComparisonServicesMixin(request)}
