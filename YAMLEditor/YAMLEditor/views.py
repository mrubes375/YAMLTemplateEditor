from django.shortcuts import render, HttpResponseRedirect, render_to_response
from django.contrib.auth import authenticate, login
from .yaml_config import get_yaml
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .serializers import UserSerializer
from .forms import RegisterForm
from tempfile import NamedTemporaryFile
from .handle import DataBindingDOM
import os


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    permission_clases = (permissions.IsAdminUser,)
    serializer_class = UserSerializer

def context_dict(request, context, function=get_yaml):
    con_dict = {'user': request.user, 'my_yaml': get_yaml()}
    fin_dict = con_dict.copy()
    fin_dict.update(context)
    return fin_dict

def render_with_yaml(request, page, context={}):
    context=context_dict(request, context)
    if request.user.is_staff:
        template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates')
        html = DataBindingDOM(template_dir, page).bind()
        rendered_file = NamedTemporaryFile(mode='r+', dir=template_dir)
        rendered_file.write(html)
        file_name = list(rendered_file.name.split('/'))[-1]
        rendered_file.read()
    else:
        file_name = page
    return render(request, file_name, context)

def c_render_to_response(template, request, status_code, context={}):
    response = render_to_response(template, context=context_dict(request, context))
    response.status_code = status_code
    return response


def index(request):
    return render_with_yaml(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = RegisterForm()
    return render_with_yaml(request, 'registration/register.html', {'form': form})


def not_found(request):
    return render_with_yaml(request, 'errors/404.html')

def server_error(request):
    return render_with_yaml(request, 'errors/500.html')

def no_access(request):
    return render_with_yaml(request, 'no_access.html')
