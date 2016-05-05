from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def client(request):
    return render(request, 'client.html', {})

def guest(request):
    return render(request, 'guest.html', {})

def login(request):
    return render(request, 'login.html', {})
