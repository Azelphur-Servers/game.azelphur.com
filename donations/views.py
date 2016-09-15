from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from .forms import DonateForm
from .models import PremiumDonation


class DonateView(FormView):
    template_name = 'donations/donate.html'
    form_class = DonateForm
    success_url = '/thanks/'

    def get_context_data(self, **kwargs):
        context = super(DonateView, self).get_context_data(**kwargs)
        context['steam'] = self._get_steam()
        try:
            context['donation'] = PremiumDonation.objects.get(user=self.request.user)
            if context['donation'].end_time > timezone.now():
                context['donation_ended'] = False
            else:
                context['donation_ended'] = True
        except PremiumDonation.DoesNotExist:
            context['donation'] = None
        return context

    def _get_steam(self):
        if self.request.user.is_authenticated():
            try:
                u = self.request.user.social_auth.filter(provider="steam").get()
                return u.uid
            except ObjectDoesNotExist:
                pass

        return None

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """

        steam = self._get_steam()
            
        domain = get_current_site(self.request).domain

        initial = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "item_name": "Donation",
            "invoice": steam,
            "notify_url": "https://" + domain + reverse('paypal-ipn'),
            "return_url": "https://game.azelphur.com/",
            "cancel_return": "https://game.azelphur.com/donate",
            "custom": steam,  # Custom command to correlate to some function later (optional)
        }

        return initial
