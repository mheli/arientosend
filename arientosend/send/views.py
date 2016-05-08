from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404

from wsgiref.util import FileWrapper

from .models import User, FileAccess, File
import StringIO

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

def download(request, key):
	template = loader.get_template('download.html')
	context = {
		'key': key,
	}
	return HttpResponse(template.render(context, request))

def retrieve(request, key):

	password = request.POST['password']

	f = File.objects.get(key=key)
	access = FileAccess.objects.get(file=f)

	if (access.password == password):
#	f = StringIO.StringIO()
#	f.write('This is a test line.\n')
		response = HttpResponse(content_type='application/octet-stream')
#		response.write(f.file.getvalue())
# TODO: find out how to get file contents
		response['Content-Disposition'] = 'attachment; filename='+password
		return response
	else:
		return HttpResponse('')

def guest(request):
	return render(request, 'guest.html', {})

def login(request):
	return render(request, 'login.html', {})
