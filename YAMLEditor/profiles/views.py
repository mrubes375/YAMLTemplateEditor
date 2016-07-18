from django.shortcuts import render

# Create your views here.
def profile_detail(request, id):
    return render(request, 'no_access.html', {
        request: request,
    })
