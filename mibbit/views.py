# Create your views here.
from mibbit.forms import MibbitForm
from django.shortcuts import render_to_response
from django.template import RequestContext

def mibbit(request):
    if request.method == 'POST': # If the form has been submitted...
        form = MibbitForm(request.POST)
        if form.is_valid():
            channels = []
            for channel in form.cleaned_data["channels"]:
                channels.append(channel.channel.replace("#", "%23"))
            channels = ",".join(channels)
            return render_to_response("mibbit.html", {'mib' : True, "channels" : channels, "znc" : form.cleaned_data["znc"]}, context_instance=RequestContext(request))
        else:
            return render_to_response("mibbit.html", {'mib' : False, "form" : form}, context_instance=RequestContext(request))
    return render_to_response("mibbit.html", {'mib' : False, "form" : MibbitForm()}, context_instance=RequestContext(request))
