from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login

def index(request):
    return render(request, 'index.html', {})

def login(request):
    # username = request.POST['username']
    # password = request.POST['password']
    # user = authenticate(username=username, passwor=password)
    # if user is not None:
    #     if user.is_active:
    #         login(request, user)
    #         return index(request)
    #     else:
    #         return HttpResponse("Disabled Account")
    # else:
    #     return HttpResponse("Invalid Login")
    return render(request, 'login.html', {})
