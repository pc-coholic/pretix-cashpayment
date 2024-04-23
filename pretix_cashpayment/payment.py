from collections import OrderedDict, namedtuple
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from django.http import HttpRequest
from django.template.loader import get_template
from django.utils.translation import gettext_lazy as _
from i18nfield.fields import I18nFormField, I18nTextarea, I18nTextInput
from i18nfield.strings import LazyI18nString
from django.utils.timezone import get_current_timezone, make_aware, now

from pretix.base.models import OrderPayment, Order, OrderPosition
from pretix.base.forms import I18nMarkdownTextarea
from pretix.base.payment import BasePaymentProvider
from pretix.base.reldate import RelativeDateWrapper
from pretix.base.reldate import ( 
    RelativeDateTimeField, RelativeDateWrapper,
)


class CashPayment(BasePaymentProvider):
    identifier = 'cashpayment'
    verbose_name = _('Cash Payment')
    abort_pending_allowed = True
    confirm_button_name = _('Confirm')


    @property
    def test_mode_message(self):
        return _('In test mode, you can just manually mark this order as paid in the backend after it has been '
                 'created.')
    
    @property
    def public_name(self) -> str:
        return str(self.settings.get("public_name", as_type=LazyI18nString) or _(
            "Cash Payment"
        ))

    @property
    def settings_form_fields(self):
<<<<<<< HEAD
        fields = [
            (
                "public_name",
                I18nFormField(
                    label=_("Payment method name"), widget=I18nTextInput, required=False
                ),
            ),
            (
                "information_text",
                I18nFormField(
                    label=_('Payment information text'),widget=I18nTextarea,
                ),
            ),
            (
                "provider_last_payment",
                RelativeDateTimeField(
                    required=False,
                    label=_('Override order expiration date'),
                    help_text=_('The order expiration date will only be changed by this setting if it is later than the date set for the event generally.'),
                )
            ),
        ]
=======
        form_field = I18nFormField(
            label=_('Payment information text'),
            widget=I18nMarkdownTextarea,
        )
>>>>>>> 4e967ce (Use I18nMarkdownTextarea)
        return OrderedDict(
            list(super().settings_form_fields.items()) + fields
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

    def execute_payment(self, request: HttpRequest, payment: OrderPayment):
        order = payment.order

        custom_expires = self.settings.get("provider_last_payment", as_type=RelativeDateWrapper)
        if custom_expires:
            if self.event.has_subevents:
                subevents = order.event.subevents.filter(id__in=order.positions.values_list('subevent_id', flat=True))
            else:
                subevents = None
            self._set_custom_expires(order, custom_expires, subevents)
    
    def _set_custom_expires(self, order: Order, reldate: RelativeDateWrapper, subevents=None):
        if reldate:
            expiry_date = order.expires

            if order.event.has_subevents and subevents:
                terms = [
                    reldate.datetime(se)
                    for se in subevents
                ]
                if not terms:
                    return
                expiry_date = min(terms)
            else:
                expiry_date = reldate.datetime(order.event)
            
            if expiry_date > order.expires:
                order.expires = expiry_date
                order.save()