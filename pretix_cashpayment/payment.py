import json
import segno
from collections import OrderedDict

from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
from i18nfield.fields import I18nFormField, I18nTextarea
from i18nfield.strings import LazyI18nString

from pretix.base.payment import BasePaymentProvider

class CashPayment(BasePaymentProvider):
    identifier = 'cashpayment'
    verbose_name =_('Cash Payment')

    @property
    def settings_form_fields(self):
        form_field = I18nFormField(
            label = _('Payment information text'),
            widget = I18nTextarea,
        )
        return OrderedDict(
            list(super().settings_form_fields.items()) + [('information_text', form_field)]
        )

    def payment_form_render(self, request) -> str:
        template = get_template('pretix_cashpayment/checkout_payment_form.html')
        ctx = {
            'request': request,
            'event': self.event,
            'information_text': self.settings.get('information_text', as_type=LazyI18nString),
        }
        return template.render(ctx)

    def checkout_prepare(self, request, total):
        return True

    def payment_is_valid_session(self, request):
        return True

    def checkout_confirm_render(self, request):
        return self.payment_form_render(request)

    def order_pending_mail_render(self, order) -> str:
        template = get_template('pretix_cashpayment/email/order_pending.txt')
        ctx = {
            'event': self.event,
            'order': order,
            'information_text': self.settings.get('information_text', as_type=LazyI18nString),
        }
        return template.render(ctx)

    def order_pending_render(self, request, order) -> str:
        template = get_template('pretix_cashpayment/pending.html')
        ctx = {
            'event': self.event,
            'order': order,
            'information_text': self.settings.get('information_text', as_type=LazyI18nString),
            'qrcode': segno.make_qr(order.full_code, error='H')
                            .png_data_uri(scale=10, border=0),
        }
        return template.render(ctx)

    def order_control_render(self, request, order) -> str:
        if order.payment_info:
            payment_info = json.loads(order.payment_info)
        else:
            payment_info = None
        template = get_template('pretix_cashpayment/control.html')
        ctx = {'request': request, 'event': self.event,
               'payment_info': payment_info, 'order': order}
        return template.render(ctx)
