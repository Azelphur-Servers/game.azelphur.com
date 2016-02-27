from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import Group
from donations.models import PremiumDonation, reload_admins
from djangobb_forum.models import Profile


class Command(BaseCommand):
    args = ''
    help = 'Remove premium from users if it has expired'

    def handle(self, *args, **options):
        donations = PremiumDonation.objects.filter(
            end_time__lte=timezone.now()
        ).delete()
        reload_admins()
