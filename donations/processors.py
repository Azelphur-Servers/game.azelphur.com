from paypal.standard.ipn.models import PayPalIPN
from django.conf import settings
from django.db.models import Sum
from decimal import Decimal
import datetime

def donations(request):
    now = datetime.datetime.now()
    amount = PayPalIPN.objects.filter(
        payment_status="Completed",
        created_at__gt=datetime.date(now.year, now.month, 1)
    ).aggregate(Sum('mc_gross'))['mc_gross__sum']
    if amount == None:
        amount = Decimal("0.0")
    amount_max = Decimal(settings.MONTHLY_DONATION_AMOUNT)
    amount_needed = amount_max-amount if amount_max-amount > 0 else 0
    context = {'donation_amount' : "%g" % (amount),
               'donation_max' : "%g" % (amount_max),
               'donation_needed' : "%g" % (amount_needed),
               'donation_percent' : "%g" % ((amount/amount_max)*100)}
    return context
