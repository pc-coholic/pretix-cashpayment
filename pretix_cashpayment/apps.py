from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from . import __version__


class PluginApp(AppConfig):
    name = 'pretix_cashpayment'
    verbose_name = 'Pretix Cash Payment plugin'

    class PretixPluginMeta:
        name = _('Cash Payment')
        author = 'Martin Gross'
        description = _('This plugin allows you to offer your customers a "pay with cash at the venue" option.')
        category = 'PAYMENT'
        visible = True
        version = __version__

    def ready(self):
        from . import signals  # NOQA


