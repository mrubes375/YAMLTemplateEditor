from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from YAMLEditor.views import c_render, no_access
from .models import Change
from datetime import datetime
# Create your views here.

def admins_only(view):
    def _decorated(request, *args, **kwargs):
        if not request.user.is_staff:
            return c_render(request, 'no_access.html')
        return view(request, *args, **kwargs)
    return _decorated

@admins_only
def log(request):
    changes = Change.objects.all().order_by('-date')
    if 'update' in request.META['PATH_INFO']:
        print(True)
    return c_render(request, 'log.html', {'changes': changes})

@admins_only
def log_details(request, id):
    change = get_object_or_404(Change, pk=id)
    return c_render(request, 'log_details.html', {'change': change})

def app(request):
    print(request.META)
    return HttpResponse('hi')
class Update:
    def __init__():
        pass
