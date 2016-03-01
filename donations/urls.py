from django.conf.urls import url, include
from .views import DonateView

urlpatterns = [
    url(r'^$', DonateView.as_view(), name='donate'),
    url(r'^ig/$', DonateView.as_view(template_name='donations/donate_ig.html'), name='donate-ig'),
]
