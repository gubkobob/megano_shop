from .cart import Cart
from .services import ComparisonServicesMixin
def cart(request):
    return {'cart': Cart(request)}

def comparison(request):
    return {'comparison': ComparisonServicesMixin(request)}
