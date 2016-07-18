from django.shortcuts import render
from django.contrib.auth import authenticate, login

def index(request):
    return render(request, 'index.html', {})

def log_in(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, passwor=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return index(request)
        else:
            return "Disabled Account"
    else:
        return "Invalid Login"
