from django.conf.urls import url, include
from .views import DonateView, KeyDonation, SteamUserExists

urlpatterns = [
    url(r'^$', DonateView.as_view(), name='donate'),
    url(r'^api/key_donation', KeyDonation.as_view(), name='key-donation'),
    url(r'^api/user_exists', SteamUserExists.as_view(), name='user_exists'),
    url(r'^ingame/tf2/$', DonateView.as_view(template_name='ingame/tf2/donate.html'), name='donate-ig'),
]
