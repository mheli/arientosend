from django.shortcuts import render, get_object_or_404
from .models import User

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def client(request):
	email = request.POST['login']
	password = request.POST['password']
	
	try:
		queryset = User.objects.get(email=email)
	except ObjectDoesNotExist:
	    return render(request, 'index.html', {})
	# Database doesn't allow duplicates on email
	#except MultipleObjectsReturned:
	#    return render(request, '404.html', {})
	else:
	    return render(request, 'client.html', {})

def guest(request):
    return render(request, 'guest.html', {})

def login(request):
    return render(request, 'login.html', {})
