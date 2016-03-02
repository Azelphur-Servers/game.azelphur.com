from django.conf.urls import url, include
from .views import DonateView

urlpatterns = [
    url(r'^$', DonateView.as_view(), name='donate'),
    url(r'^ingame/tf2/$', DonateView.as_view(template_name='ingame/tf2/donate.html'), name='donate-ig'),
]
