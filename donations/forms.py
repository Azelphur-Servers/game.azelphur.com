from django import forms
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm


class DonateForm(PayPalPaymentsForm):
    amount = forms.ChoiceField(
        choices=[(x[0], str(x[1])+" days") for x in settings.DONATION_AMOUNTS]
    )
