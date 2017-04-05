from __future__ import unicode_literals
from .decorators import get_cart_from_request


def cart_counter(request):
    """ Return number of items from cart """
    cart = get_cart_from_request(request)
    cart_quantity = cart.quantity
    if cart_quantity>0:
        cart_total = cart.get_total().gross
    else:
        cart_total = 0
    return {'cart_counter': cart_quantity, 'cart_total': cart_total}
