from django import forms
from mibbit.models import IRCChannel

class MibbitForm(forms.Form):
    channels = forms.ModelMultipleChoiceField(
        queryset=IRCChannel.objects.all(),
        initial=IRCChannel.objects.filter(default=True),
        widget=forms.CheckboxSelectMultiple()
    )
    znc = forms.BooleanField(
        required=False,
        help_text="Leave this off unless you have a ZNC account"
    )
