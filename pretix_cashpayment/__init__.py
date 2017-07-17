from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class PluginApp(AppConfig):
    name = 'pretix_cashpayment'
    verbose_name = 'Pretix Cash Payment plugin'

    class PretixPluginMeta:
        name = _('Cash Payment')
        author = 'Martin Gross'
        description = _('This plugin allows you to offer your customers a "pay with cash at the venue" option.')
        visible = True
        version = '1.0.0'

    def ready(self):
        from . import signals  # NOQA


default_app_config = 'pretix_cashpayment.PluginApp'
