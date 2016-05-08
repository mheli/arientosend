from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404

from .models import User, FileAccess

# Create your views here.
def index(request):
	return render(request, 'index.html', {})

def client(request):
	email = request.POST['login']
	password = request.POST['password']
	
	try:
		user = User.objects.get(email=email)
	except ObjectDoesNotExist:
		return render(request, 'index.html', {})
	# Database doesn't allow duplicates on email
	#except MultipleObjectsReturned:
	#    return render(request, '404.html', {})
	else:
		# assumes ariento user is set when an ariento user
		# is receiving and when sending
		inbox_list = FileAccess.objects.filter(ariento_user=user).exclude(file_from_email=user.email)
		outbox_list = FileAccess.objects.filter(file_from_email=user.email)
		context = {
			'inbox_list': inbox_list,
			'outbox_list': outbox_list,
		}
		template = loader.get_template('client.html')
		return HttpResponse(template.render(context, request))

def guest(request):
	return render(request, 'guest.html', {})

def login(request):
	return render(request, 'login.html', {})
