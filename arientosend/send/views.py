from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import Storage
from django.core.files import File
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from wsgiref.util import FileWrapper

from .models import User, FileAccess
from .models import File as ArientoFile

import hashlib
from .mailer import emailer

emailer = emailer()

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
	else:
		# assumes ariento user is set when an ariento user
		# is receiving and when sending
		inbox_list = FileAccess.objects.filter(recipient_email=user.email)
		outbox_list = FileAccess.objects.filter(sender_email=user.email)
		context = {
			'inbox_list': inbox_list,
			'outbox_list': outbox_list,
		}
		template = loader.get_template('client.html')
		return HttpResponse(template.render(context, request))

def client_send(request):
	recipient = request.POST['email']
	password = request.POST['password']
	message = request.POST['message']
	# can only get one file at a time
	attachment = request.FILES['attachments']

	af = ArientoFile()
	af.file=attachment
	af.save()

	fa = FileAccess()
	fa.file = af
	fa.recipient_email = recipient
	fa.sender_email = 'test@ariento.com'
	try:
		u = User.objects.get(email=recipient)
	except ObjectDoesNotExist:
		fa.access_type = 'P'
		fa.password = password
	else:
		fa.access_type = 'U'
		fa.ariento_user = u
	finally:
		fa.save()
        
                email_body = '''An ariento guest, %s, has sent you a file.\nClick here to download it:http://ec2-54-172-241-8.compute-1.amazonaws.com/download/%s/\nMessage:%s''' % (str(af.id) , fa.sender_email, message)
                emailer.sendmail(recipient, "Ariento File Send", email_body)
        
		context = {
			'recipient': recipient,
			'num_files': af.id,
		}
		template = loader.get_template('success.html')
		return HttpResponse(template.render(context, request))

def download(request, key):
	try:
		arientoFile = ArientoFile.objects.get(id=key)
		access = FileAccess.objects.get(file=arientoFile)
	except ObjectDoesNotExist:
		template = loader.get_template('filenotfound.html')
		context = {
			'not_found_type': 'does_not_exist',
		}
		return HttpResponse(template.render(context, request))
	else:
		if (access.access_type == 'P'):
			return render(request, 'download.html', {})
		else:
			template = loader.get_template('filenotfound.html')
			context = {
				'not_found_type': 'does_not_exist',
			}
			return HttpResponse(template.render(context, request))

def retrieve(request, key):
	password = request.POST['password']
	try:
		arientoFile = ArientoFile.objects.get(id=key)
		access = FileAccess.objects.get(file=arientoFile)
	except ObjectDoesNotExist:
		template = loader.get_template('filenotfound.html')
		context = {
			'not_found_type': 'does_not_exist',
		}
		return HttpResponse(template.render(context, request))
	else:
		if (access.file_expiration_date <= timezone.now() or access.download_count >= access.download_limit):
			arientoFile.delete()
			template = loader.get_template('filenotfound.html')
			context = {
				'not_found_type': 'does_not_exist',
			}
			return HttpResponse(template.render(context, request))
		elif (access.password == password):
			# increase download count
			access.download_count = access.download_count + 1
			access.save()

			response = HttpResponse(content_type='application/octet-stream')
			response['Content-Disposition'] = 'attachment; filename='+arientoFile.file.name
			response.write(arientoFile.file.read())
			return response
		else:
			template = loader.get_template('filenotfound.html')
			context = {
				'not_found_type': 'incorrect_password',
			}
			return HttpResponse(template.render(context, request))

def guest(request):
	return render(request, 'guest.html', {})

def guest_send(request):
	name = request.POST['name']
	sender = request.POST['guestEmail']
	recipient = request.POST['email']
	message = request.POST['message']
	# only gets one file upload even if multiple are sent
	attachment = request.FILES['attachments']

	try:
		u = User.objects.get(email=recipient)
	except ObjectDoesNotExist:
		return render(request, 'guest.html', {})
	else:
		af = ArientoFile()
		af.file=attachment
		af.save()

		fa = FileAccess()
		fa.file = af
		fa.access_type = 'U'
		fa.ariento_user = u
		fa.sender_email = sender
		fa.recipient_email = recipient
		fa.save()

                email_body = '''An ariento guest, %s, has sent you a file.\nClick here to download it:http://ec2-54-172-241-8.compute-1.amazonaws.com/download/%s/\nMessage:%s''' % (str(af.id) , sender, message)
                emailer.sendmail(recipient, "Ariento File Send", email_body)
        
		context = {
			'recipient': recipient,
			'num_files': af.id,
		}
		template = loader.get_template('success.html')
		return HttpResponse(template.render(context, request))

def login(request):
	return render(request, 'login.html', {})

def user_download(request):
	key = request.POST['key']
	try:
		arientoFile = ArientoFile.objects.get(id=key)
		access = FileAccess.objects.get(file=arientoFile)
	except ObjectDoesNotExist:
		template = loader.get_template('filenotfound.html')
		context = {
			'not_found_type': 'does_not_exist',
		}
		return HttpResponse(template.render(context, request))
	else:
		if (access.file_expiration_date <= timezone.now() or access.download_count >= access.download_limit):
			arientoFile.delete()
			template = loader.get_template('filenotfound.html')
			context = {
				'not_found_type': 'does_not_exist',
			}
			return HttpResponse(template.render(context, request))
		else:
			# increase download count
			access.download_count = access.download_count + 1
			access.save()

			response = HttpResponse(content_type='application/octet-stream')
			response['Content-Disposition'] = 'attachment; filename='+arientoFile.file.name
			response.write(arientoFile.file.read())
			return response
