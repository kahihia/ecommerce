from django.conf import settings
from django.template.response import TemplateResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from ..product.models import Product


def home(request):
    products = Product.objects.get_available_products()[:12]
    products = products.prefetch_related('categories', 'images',
                                         'variants__stock')
    return TemplateResponse(
        request, 'base.html',
        {'products': products, 'parent': None})

def contact(request):

    return TemplateResponse(
        request, 'contact.html')

def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response
