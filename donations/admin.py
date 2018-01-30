from django.contrib import admin
from .models import PremiumDonation
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ('user',)

class PremiumDonationAdmin(admin.ModelAdmin):
    list_display = ('user', 'end_time')

admin.site.register(PremiumDonation, PremiumDonationAdmin)
