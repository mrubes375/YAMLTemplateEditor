from django.shortcuts import render
from YAMLEditor.views import c_render
from .models import Change
# Create your views here.
def log(request):
    obj = Change.objects.all()
    return c_render(request, 'log.html', {'obj': obj})
