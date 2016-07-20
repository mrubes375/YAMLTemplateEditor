from django.shortcuts import render
from YAMLEditor.views import c_render
from .models import Change
from datetime import datetime
# Create your views here.
def log(request):
    changes = Change.objects.all()
    return c_render(request, 'log.html', {'changes': changes})

def log_details(request, id):
    change = Change.objects.get(pk=id)
    return c_render(request, 'log_details.html', {'change': change})
