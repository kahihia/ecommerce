import datetime

from mock import Mock

from saleor.product import models


def test_stock_selector(product_in_stock):
    variant = product_in_stock.variants.get()
    preferred_stock = variant.select_stockrecord(5)
    assert preferred_stock.quantity_available >= 5


def test_stock_allocator(product_in_stock):
    variant = product_in_stock.variants.get()
    stock = variant.select_stockrecord(5)
    assert stock.quantity_allocated == 0
    models.Stock.objects.allocate_stock(stock, 1)
    stock = models.Stock.objects.get(pk=stock.pk)
    assert stock.quantity_allocated == 1


def test_product_page_redirects_to_correct_slug(client, product_in_stock):
    uri = product_in_stock.get_absolute_url()
    uri = uri.replace(product_in_stock.get_slug(), 'spanish-inquisition')
    response = client.get(uri)
    assert response.status_code == 301
    location = response['location']
    if location.startswith('http'):
        location = location.split('http://testserver')[1]
    assert location == product_in_stock.get_absolute_url()


def test_product_preview(admin_client, client, product_in_stock):
    product_in_stock.available_on = (
        datetime.date.today() + datetime.timedelta(days=7))
    product_in_stock.save()
    response = client.get(product_in_stock.get_absolute_url())
    assert response.status_code == 404
    response = admin_client.get(product_in_stock.get_absolute_url())
    assert response.status_code == 200


def test_product_page_without_openexchagerates(
        client, product_in_stock, settings):
    settings.OPENEXCHANGERATES_API_KEY = None
    response = client.get(product_in_stock.get_absolute_url())
    context = response.context
    assert context['local_price_range'] is None


def test_product_page_with_openexchagerates(
        client, monkeypatch, product_in_stock, settings):
    settings.DEFAULT_CURRENCY = 'USD'
    settings.DEFAULT_COUNTRY = 'PL'
    settings.OPENEXCHANGERATES_API_KEY = 'fake-key'
    response = client.get(product_in_stock.get_absolute_url())
    context = response.context
    assert context['local_price_range'] is None
    monkeypatch.setattr(
        'django_prices_openexchangerates.models.get_rates',
        lambda c: {'PLN': Mock(rate=2)})
    response = client.get(product_in_stock.get_absolute_url())
    context = response.context
    assert context['local_price_range'].min_price.currency == 'PLN'
