from django.shortcuts import render, HttpResponseRedirect, render_to_response
from django.contrib.auth import authenticate, login
from .yaml_config import get_yaml
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer
from .forms import RegisterForm


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

def context_dict(request, context, function=get_yaml):
    con_dict = {'user': request.user, 'my_yaml': get_yaml()}
    fin_dict = con_dict.copy()
    fin_dict.update(context)
    return fin_dict

def c_render(request, page, context={}):
    context=context_dict(request, context)
    print(context)
    return render(request, page, context)

def c_render_to_response(template, request, status_code, context={}):
    response = render_to_response(template, context=context_dict(request, context))
    response.status_code = status_code
    return response


def index(request):
    return c_render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = RegisterForm()
    return c_render(request, 'registration/register.html', {'form': form})


def not_found(request):
    return c_render(request, 'errors/404.html')

def server_error(request):
    return c_render(request, 'errors/500.html')

def no_access(request):
    return c_render(request, 'no_access.html')
