from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from .forms import DonateForm


class DonateView(FormView):
    template_name = 'donations/donate.html'
    form_class = DonateForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super(ContactView, self).form_valid(form)


    def get_context_data(self, **kwargs):
        context = super(DonateView, self).get_context_data(**kwargs)
        try:
            context['steam'] = self.request.user.social_auth.filter(
                provider="steam").get()
        except ObjectDoesNotExist:
            context['steam'] = None
        return context


    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """

        try:
            u = self.request.user.social_auth.filter(provider="steam").get()
            steam = u.uid
        except ObjectDoesNotExist:
            steam = ""

        domain = get_current_site(self.request).domain

        initial = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "item_name": "Donation",
            "invoice": steam,
            "notify_url": "https://" + domain + reverse('paypal-ipn'),
            "return_url": "https://www.example.com/your-return-location/",
            "cancel_return": "https://www.example.com/your-cancel-location/",
            "custom": steam,  # Custom command to correlate to some function later (optional)
        }

        return initial
