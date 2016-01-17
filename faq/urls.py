from django.conf.urls import url
from .views import FAQListView

urlpatterns = [
    url(r'^', FAQListView.as_view(), name='faq'),
]
