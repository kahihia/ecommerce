from django.utils.translation import pgettext_lazy


class Status(object):
    NEW = 'new'
    CANCELLED = 'cancelled'
    SHIPPED = 'shipped'
    PAYMENT_PENDING = 'payment-pending'
    FULLY_PAID = 'fully-paid'

    CHOICES = [
        (NEW, pgettext_lazy('order status', 'Processando')),
        (CANCELLED, pgettext_lazy('order status', 'Cancelada')),
        (SHIPPED, pgettext_lazy('order status', 'Enviada')),
        (PAYMENT_PENDING, pgettext_lazy('order status', 'Pagamento pendente')),
        (FULLY_PAID, pgettext_lazy('order status', 'Pago'))]
