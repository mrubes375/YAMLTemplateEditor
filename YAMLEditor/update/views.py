from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from YAMLEditor.views import render_with_yaml, no_access
from update.serializers import ChangeSerializer
from .models import Change
import os
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from YAMLEditor.handle import ChangeYAML, FileSearcher
import json
# Create your views here.

template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates')
class ChangeViewSet(viewsets.ModelViewSet):
    queryset = Change.objects.all().order_by('-date')
    serializer_class = ChangeSerializer

@csrf_exempt
def ajax_context(request):
    if request.is_ajax():
        data = json.loads(request.body.decode('utf-8'))
        tag = data['tag'].strip()
        new_context = data['new_context'].strip()
        old_context = ChangeYAML(tag, new_context).update()
        user = request.user
        search = FileSearcher()
        files_changed = ', '.join(search.get_files_changed(tag))
        change = Change(files_changed=files_changed, user=user, template=tag, old_context=old_context, new_context=new_context)
        change.save()
        
        return HttpResponse(data)
    else:
        return render_with_yaml(request, 'errors/404.html')

def admins_only(view):
    def _decorated(request, *args, **kwargs):
        if not request.user.is_staff:
            injected_template = some_function('no_access.html')
            return render_with_yaml(request, 'no_access.html')
        return view(request, *args, **kwargs)
    return _decorated

@admins_only
def log(request):
    changes = Change.objects.all().order_by('-date')
    return render_with_yaml(request, 'log.html', {'changes': changes})

@admins_only
def log_details(request, id):
    change = get_object_or_404(Change, pk=id)
    return render_with_yaml(request, 'log_details.html', {'change': change})

def app(request):
    print(request.META)
    return HttpResponse('hi')

class Update:
    def __init__():
        pass
