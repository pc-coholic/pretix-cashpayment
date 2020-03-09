from collections import OrderedDict

from django.http import HttpRequest
from django.template.loader import get_template
from django.utils.translation import gettext_lazy as _
from i18nfield.fields import I18nFormField, I18nTextarea
from i18nfield.strings import LazyI18nString

from pretix.base.models import OrderPayment
from pretix.base.payment import BasePaymentProvider


class CashPayment(BasePaymentProvider):
    identifier = 'cashpayment'
    verbose_name = _('Cash Payment')
    abort_pending_allowed = True

    @property
    def test_mode_message(self):
        return _('In test mode, you can just manually mark this order as paid in the backend after it has been '
                 'created.')

    @property
    def settings_form_fields(self):
        form_field = I18nFormField(
            label=_('Payment information text'),
            widget=I18nTextarea,
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

    def payment_pending_render(self, request: HttpRequest, payment: OrderPayment):
        template = get_template('pretix_cashpayment/pending.html')
        ctx = {
            'event': self.event,
            'order': payment.order,
            'information_text': self.settings.get('information_text', as_type=LazyI18nString),
        }
        return template.render(ctx)

    def payment_control_render(self, request: HttpRequest, payment: OrderPayment):
        template = get_template('pretix_cashpayment/control.html')
        ctx = {'request': request, 'event': self.event,
               'payment_info': payment.info_data, 'order': payment.order}
        return template.render(ctx)
