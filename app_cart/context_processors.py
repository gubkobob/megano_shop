from .cart import Cart, get_cart
from .services import ComparisonServicesMixin
def cart(request):
    return {'cart': Cart(request)}

def comparison(request):
    return {'comparison': ComparisonServicesMixin(request)}
