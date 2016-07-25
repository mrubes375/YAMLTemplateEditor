from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from YAMLEditor.views import c_render, no_access
from update.serializers import ChangeSerializer
from .models import Change
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from .handle import Handler
import json
# Create your views here.

class ChangeViewSet(viewsets.ModelViewSet):
    queryset = Change.objects.all().order_by('-date')
    serializer_class = ChangeSerializer

@csrf_exempt
def ajax_context(request):
    if request.is_ajax():
        data = json.loads(request.body.decode('utf-8'))
        old_context = data['old_context'].strip()
        new_context = data['new_context'].strip()
        handle = Handler()
        print(handle.get_yaml()['navbar']['name'])

    else:
        message = "Nah"
    return HttpResponse('hi')

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
