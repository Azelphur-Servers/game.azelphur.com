DISPLAY_NAMES = {
    'reddit': 'Reddit',
    'github': 'Github',
    'google-oauth2': 'Google',
    'facebook': 'Facebook',
    'twitter': 'Twitter',
}

def social_display_name(value):
    return DISPLAY_NAMES.get(value.lower(), value)
