from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from djangobb_forum.models import Profile
from djangobb_forum import settings as forum_settings

def staff(request):
    staffMembers = []
    for user in User.objects.filter(is_staff=True).extra(select = {'lower_username': 'lower(username)'}).order_by("lower_username"):
        steamID = ''
        try:
            steamID = user.social_auth.filter(provider="steam").get().uid
        except ObjectDoesNotExist:
            pass
        staffMembers.append({'user': user, 'steamID': steamID})
    return render_to_response('ingame/tf2/staff.html', {'staff': staffMembers, 'forum_settings': forum_settings, 'request': request})


# Used to look up dictionary values by key in the radio template
# Credit to http://stackoverflow.com/a/8000091/1306662
from django.template.defaulttags import register
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def radio(request):
    radioStations = {
        'rock': {'name': 'Rock/Pop', 'url': '99.198.118.250:8076'},
        'dubstep': {'name': 'DubStep', 'url': '173.239.76.147:8400'},
        'alternative': {'name': 'Alternative', 'url': '205.164.62.20:8070'},
        'top40': {'name': 'Top 40', 'url': '85.17.121.216:8428'},
        'classicrock': {'name': 'Classic Rock', 'url': '192.240.102.5:7025'},
        'pop': {'name': 'Pop/Dance', 'url': '5.135.191.40:8000'},
        'metal': {'name': 'Metal', 'url': '69.4.232.118:80'},
        'hiphop': {'name': 'Hip Hop', 'url': '91.121.1.157:9242'},
        'country': {'name': 'Country', 'url': '205.164.35.139:80'},
        'blues': {'name': 'Blues', 'url': '50.7.77.114:8351'},
        'jazz': {'name': 'Jazz', 'url': '192.99.35.93:6402'},
        'classical': {'name': 'Classical', 'url': '174.36.206.197:8000'}
    }
    r = request.GET.get('r')
    if r not in radioStations:
        r = None
    return render_to_response('ingame/tf2/radio.html', {'request': request, 'r': r, 'radioStations': radioStations})
