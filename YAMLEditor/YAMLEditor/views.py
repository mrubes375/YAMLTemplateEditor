from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .serializers import UserSerializer
from .forms import RegisterForm, LoginForm
from Render.render import c_render_to_response, render_with_yaml

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    permission_clases = (permissions.IsAdminUser,)
    serializer_class = UserSerializer

def index(request):
    return render_with_yaml(request, 'index.html')

def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(request.POST['password'])
            user.save()
            new_user = authenticate(username=request.POST['username'], password=request.POST['password'])
            new_user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, new_user)
            return HttpResponseRedirect('/')
    else:
        form = RegisterForm()
    return render_with_yaml(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        login(request, user)
        return HttpResponseRedirect('/')
    else:
        form = LoginForm()
    return render_with_yaml(request, 'registration/login.html', {'form': form})

def about(request):
    return render_with_yaml(request, 'about.html')

def not_found(request):
    return render_with_yaml(request, 'errors/404.html')

def server_error(request):
    return render_with_yaml(request, 'errors/500.html')

def no_access(request):
    return render_with_yaml(request, 'no_access.html')
