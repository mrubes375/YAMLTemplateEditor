from django.shortcuts import render, HttpResponse, render_to_response
from django.contrib.auth import authenticate, login
from .yaml_config import get_yaml
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer
from .forms import LoginForm


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

def context_dict(request, context):
    con_dict = {'user': request.user, 'my_yaml': get_yaml()}
    fin_dict = con_dict.copy()
    fin_dict.update(context)
    return fin_dict

def c_render(request, page, context={}):
    return render(request, page, context=context_dict(request, context))

def c_render_to_response(template, request, status_code, context={}):
    response = render_to_response(template, context=context_dict(request, context))
    response.status_code = status_code
    return response


def index(request):
    return c_render(request, 'index.html')

def login(request):

    form = LoginForm
    return c_render(request, 'login.html', {'form': form})


def not_found(request):
    return c_render(request, 'errors/404.html')

def server_error(request):
    return c_render(request, 'errors/500.html')

def no_access(request):
    return c_render(request, 'no_access.html')
