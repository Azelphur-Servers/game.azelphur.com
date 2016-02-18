from django import template 

register = template.Library()

DISPLAY_NAMES = {
    'reddit': 'Reddit',
    'github': 'Github',
    'google-oauth2': 'Google',
    'facebook': 'Facebook',
    'twitter': 'Twitter',
}

@register.filter(name='social_display_name')
def social_display_name(value):
    return DISPLAY_NAMES.get(value.lower(), value)
