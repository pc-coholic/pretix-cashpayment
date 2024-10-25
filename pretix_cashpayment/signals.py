from django.dispatch import receiver
from django.utils.translation import gettext_noop
from i18nfield.strings import LazyI18nString
from pretix.base.settings import settings_hierarkey
from pretix.base.signals import (
    api_event_settings_fields, register_payment_providers,
)
from rest_framework import serializers


@receiver(register_payment_providers, dispatch_uid="payment_cash")
def register_payment_provider(sender, **kwargs):
    from .payment import CashPayment
    return CashPayment


@receiver(api_event_settings_fields, dispatch_uid="cashpayment_api_event_settings_fields")
def api_event_settings_fields(sender, **kwargs):
    return {
        'payment_cashpayment__enabled': serializers.BooleanField(required=False),
    }


settings_hierarkey.add_default('payment_cashpayment_information_text', LazyI18nString.from_gettext(gettext_noop(
    "You can pay your order by cash at the venue."
)), LazyI18nString)
