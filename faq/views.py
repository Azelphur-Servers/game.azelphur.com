# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from faq.models import FAQ

def faq(request):
    return render_to_response("faq.html",   
        {'faqs': FAQ.objects.all()},
        context_instance=RequestContext(request)
    )
