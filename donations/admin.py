from django.contrib import admin
from .models import PremiumDonation

class PremiumDonationAdmin(admin.ModelAdmin):
    list_display = ('user', 'end_time')

admin.site.register(PremiumDonation, PremiumDonationAdmin)
