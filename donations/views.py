from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from .forms import DonateForm
from .models import PremiumDonation
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import KeyDonationSerializer
from social.apps.django_app.default.models import UserSocialAuth
from datetime import timedelta
import uuid


class DonateView(FormView):
    template_name = 'donations/donate.html'
    form_class = DonateForm
    success_url = '/thanks/'

    def get_context_data(self, **kwargs):
        context = super(DonateView, self).get_context_data(**kwargs)
        context['steam'] = self._get_steam()
        if self.request.user.is_authenticated():
            try:
                context['donation'] = PremiumDonation.objects.filter(user=self.request.user).last()
                if context['donation'].end_time > timezone.now():
                    context['donation_ended'] = False
                else:
                    context['donation_ended'] = True
            except PremiumDonation.DoesNotExist:
                context['donation'] = None
        else:
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
            "invoice": str(steam)+":"+uuid.uuid4().hex,
            "notify_url": "https://" + domain + reverse('paypal-ipn'),
            "return_url": "https://game.azelphur.com/",
            "cancel_return": "https://game.azelphur.com/donate",
            "custom": steam,  # Custom command to correlate to some function later (optional)
        }

        return initial


class KeyDonation(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = KeyDonationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                social_user = UserSocialAuth.objects.get(uid=serializer.data["steamid64"])
            except ObjectDoesNotExist:
                # Todo: do something here as something has gone wrong
                return Response({"steamid64": "user does not exist"}, status=status.HTTP_404_NOT_FOUND)
            for x in settings.KEY_AMOUNTS:
                if x[0] == serializer.data["amount"]:
                    end_time = timezone.now() + timedelta(days=x[1])
                    PremiumDonation(
                        user=social_user.user,
                        end_time=end_time
                    ).save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"amount": "amount does not match anything in settings.KEY_AMOUNTS"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
