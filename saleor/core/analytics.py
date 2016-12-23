import uuid

from django.conf import settings
import google_measurement_protocol as ga

FINGERPRINT_PARTS = [
    'HTTP_ACCEPT_ENCODING',
    'HTTP_ACCEPT_LANGUAGE',
    'HTTP_USER_AGENT',
    'HTTP_X_FORWARDED_FOR',
    'REMOTE_ADDR']

UUID_NAMESPACE = uuid.UUID('fb4abc05-e2fb-4e3e-8b78-28037ef7d07f')


def get_client_id(request):
    parts = [request.META.get(key, '') for key in FINGERPRINT_PARTS]
    return uuid.uuid5(UUID_NAMESPACE, '_'.join(parts))


def _report(client_id, what, extra_info=None, extra_headers=None):
    tracking_id = getattr(settings, 'GOOGLE_ANALYTICS_TRACKING_ID', None)
    if tracking_id and client_id:
        ga.report(tracking_id, client_id, what, extra_info=extra_info,
                  extra_headers=extra_headers)


def report_view(client_id, path, language, headers):
    host_name = headers.get('HTTP_HOST', None)
    referrer = headers.get('HTTP_REFERER', None)
    pv = ga.PageView(path, host_name=host_name, referrer=referrer)
    extra_info = ga.SystemInfo(language=language)
    extra_headers = {}
    """
    if '/products/' in path and '/category/' not in path and '.jpg' not in path and '.png' not in path:
        print('here')

        extra_info = [{'ecommerce': {
                       'detail': {
                         'actionField': {'list': 'Apparel Gallery'},
                         'products': [{
                           'name': 'Triblend Android T-Shirt',
                           'id': '12345',
                           'price': '15.25',
                           'brand': 'Google',
                           'category': 'Apparel',
                           'variant': 'Gray'
                          }]
                        }}}]
    """



    user_agent = headers.get('HTTP_USER_AGENT', None)
    if user_agent:
        extra_headers['user-agent'] = user_agent
    _report(client_id, pv, extra_info=extra_info, extra_headers=extra_headers)

    """
    if '/cart/add/' in path:

        extra_info = [{'ecommerce': {
                        'currencyCode': 'EUR',
                        'add': {
                          'products': [{
                            'name': 'Triblend Android T-Shirt',
                            'id': '12345',
                            'price': '15.25',
                            'brand': 'Google',
                            'category': 'Apparel',
                            'variant': 'Gray',
                            'quantity': 1
                           }]
                        }
                      }}]

        event = ga.Event('ecommerce', 'addToCart')
        _report(client_id, event, extra_info=extra_info, extra_headers=extra_headers)
    elif '/checkout/shipping-address/' in path:

        extra_info = [
                          {'step': 1,
                          'option': 'Visa',
                          'products': {
                            'name': 'Triblend Android T-Shirt',
                            'id': '12345',
                            'price': '15.25',
                            'brand': 'Google',
                            'category': 'Apparel',
                            'variant': 'Gray',
                            'quantity': 1
                         }
                       }]

        event = ga.Event('ecommerce', 'checkout')
        _report(client_id, event, extra_info=extra_info, extra_headers=extra_headers)
    """



def report_order(client_id, order):
    for group in order:
        """
        items = [ga.Item(oi.product.name,
                         oi.get_price_per_item(),
                         quantity=oi.quantity,
                         item_id=oi.product_sku)
                 for oi in group]
        """
        items = [ga.EnhancedItem(oi.product.name,
                                 oi.get_price_per_item().gross,
                                 quantity=oi.quantity,
                                 item_id=oi.product_sku,
                                 category=oi.product.categories.first().name,
                                 brand='Luana Vizzon Acessórios',
                                 variant=oi.product_name)
                 for oi in group]
        #for oi in group:
        #    print(oi.get_price_per_item().gross)
        """
        trans = ga.Transaction('%s-%s' % (order.id, group.id), items,
                               revenue=group.get_total(),
                               shipping=group.shipping_price)
        """
        trans = ga.EnhancedPurchase('%s-%s' % (order.id, group.id),
                                    items,
                                    url_page = '/checkout/payment/',
                                    revenue=group.get_total(),
                                    shipping=group.shipping_price)

        _report(client_id, trans, {})
