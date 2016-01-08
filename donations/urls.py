from django.conf.urls import url, include
from .views import DonateView

urlpatterns = [
    url(r'^', DonateView.as_view(), name='donate'),
]
