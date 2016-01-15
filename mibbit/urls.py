from django.conf.urls import url, include
from .views import mibbit

urlpatterns = [
    url(r'^', mibbit, name='chat'),
]
