from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import Storage
from django.core.files import File
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from django.core import serializers
from django.template.loader import render_to_string
from wsgiref.util import FileWrapper

from .models import User, FileAccess
from .models import File as ArientoFile

from .SafeNet import SafeNet

import re

import hashlib, uuid
import json
from .mailer import emailer

emailer = emailer()

#####################
# Helper functions
#####################
def get_salt():
	return uuid.uuid1().hex

def hashed_password(password, salt):
	return hashlib.sha512(password+salt).hexdigest()

def response_file_not_found(request, message='does_not_exist'):
	template = loader.get_template('filenotfound.html')
	context = {
		'not_found_type': message,
	}
	return HttpResponse(template.render(context, request))

def response_login_not_found(request, message='login_not_found'):
	template = loader.get_template('login.html')
	context = {
		'not_found_type': message,
	}
	return HttpResponse(template.render(context, request))

def response_recipient_not_found(request, message='recipient_not_found'):
	template = loader.get_template('guest.html')
	context = {
		'not_found_type': message,
	}
	return HttpResponse(template.render(context, request))

def validate_email(email, message='invalid_input'):
	if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
		template = loader.get_template('filenotfound.html')
		context = {
			'invalid_input': message,
		}
		return HttpResponse(template.render(context, request))	
	return None

#####################
# Create your views here.
#####################
def index(request):
	if 'authorized_user' in request.session:
		return redirect('/client')
	else:
		return render(request, 'index.html', {})

def client(request):
	if 'authorized_user' in request.session:
		email = request.session['authorized_user']
		try:
			user = User.objects.get(email=email)
		except ObjectDoesNotExist:
			del request.session['authorized_user']
			return render(request, 'login.html', {})
	else:
                safenet = SafeNet()
		try:
			email = request.POST['login']
			# TODO: SafeNet authentication
			password = request.POST['password']
                        if not safenet.authenticate(email, password):
                            return render(request, 'login.html', {})

		except KeyError:
			return render(request, 'login.html', {})

		try:
			user = User.objects.get(email=email)
		except ObjectDoesNotExist:
			return response_login_not_found(request)
		else:
			request.session['authorized_user'] = email

	inbox_list = FileAccess.objects.filter(recipient_email=user.email)
	outbox_list = FileAccess.objects.filter(sender_email=user.email)
	
	user_email = user.email
        context = {
		'inbox_list': inbox_list,
		'outbox_list': outbox_list,
        'user_email' : user_email,
	}
	template = loader.get_template('client.html')
	return HttpResponse(template.render(context, request))

def client_send(request):
	email = ""
	if 'authorized_user' in request.session:
		email = request.session['authorized_user']
		try:
			user = User.objects.get(email=email)
		except ObjectDoesNotExist:
			del request.session['authorized_user']
			return render(request, 'login.html', {})
	else:
		return render(request, 'login.html', {})

	try:
		recipient = request.POST['email']
		password = request.POST['password']
		message = request.POST['message']
		attachment = request.FILES.getlist('attachments')
		
		#validate emails
		if validate_email(recipient):
			return(validate_email(recipient))
		if validate_email(email):
			return(validate_email(email)) 
	except KeyError:
		return redirect('/client')
	else:
		client_is_recipient = False
		sent_to_client = False
		for attached in attachment:
			af = ArientoFile()
			af.file=attached
			af.save()

			fa = FileAccess()
			fa.file = af
				
			fa.recipient_email = recipient
			fa.sender_email = email
			try:
				u = User.objects.get(email=recipient)
			except ObjectDoesNotExist:
				fa.access_type = 'P'
				fa.salt = get_salt()
				fa.hashed_password = hashed_password(password, fa.salt)
				email_body = '''An Ariento client, %s, has sent you a file.\nClick here to download it:http://ec2-54-172-241-8.compute-1.amazonaws.com/download/%s/\nMessage:%s''' % (fa.sender_email, str(af.id), message)
			else:
				fa.access_type = 'U'
				fa.ariento_user = u
				email_body = '''An Ariento client, %s, has sent you a file.\nLog in to download it:http://ec2-54-172-241-8.compute-1.amazonaws.com/login\nMessage:%s''' % (fa.sender_email, message)
				client_is_recipient = True
			finally:
				fa.save()

				if (client_is_recipient and not sent_to_client):
					emailer.sendmail(recipient, "Ariento File Send", email_body)
					sent_to_client = True
				elif (client_is_recipient and sent_to_client):
					pass
				else:
					emailer.sendmail(recipient, "Ariento File Send", email_body)

		context = {
			'recipient': recipient,
			'num_files': len(attachment),
		}
		template = loader.get_template('success.html')
		return HttpResponse(template.render(context, request))

def download(request, key):
	try:
		arientoFile = ArientoFile.objects.get(id=key)
		access = FileAccess.objects.get(file=arientoFile)
	except ObjectDoesNotExist:
		return response_file_not_found(request)
	else:
		if (access.access_type == 'P'):
			return render(request, 'download.html', {})
		else:
			return response_file_not_found(request)

def retrieve(request, key):
	try:
		password = request.POST['password']
	except KeyError:
		return response_file_not_found(request, 'incorrect_password')
	else:
		try:
			arientoFile = ArientoFile.objects.get(id=key)
			access = FileAccess.objects.get(file=arientoFile)
		except ObjectDoesNotExist:
			return response_file_not_found(request)
		else:
			if (access.file_expiration_date <= timezone.now() or access.download_count >= access.download_limit):
				arientoFile.delete()
				return response_file_not_found(request)
			elif (access.hashed_password == hashed_password(password, access.salt)):
				# increase download count
				access.download_count = access.download_count + 1
				access.save()

				response = HttpResponse(content_type='application/octet-stream')
				response['Content-Disposition'] = 'attachment; filename='+arientoFile.file.name
				response.write(arientoFile.file.read())
				return response
			else:
				return response_file_not_found(request, 'incorrect_password')

def guest(request):
	return render(request, 'guest.html', {})

def guest_send(request):
	try:
		name = request.POST['name']
		sender = request.POST['guestEmail']
		recipient = request.POST['email']
		message = request.POST['message']
		attachment = request.FILES.getlist('attachments')
		
		#validate emails
		if validate_email(recipient):
			return(validate_email(recipient))
		if validate_email(sender):
			return(validate_email(sender))				
		
	except KeyError:
		return render(request, 'guest.html', {})
	else:
		try:
			u = User.objects.get(email=recipient)
		except ObjectDoesNotExist:
			return response_recipient_not_found(request)
		else:
			for attached in attachment:
				af = ArientoFile()
				af.file=attached
				af.save()

				fa = FileAccess()
				fa.file = af
				fa.access_type = 'U'
				fa.ariento_user = u
				fa.sender_email = sender
				fa.recipient_email = recipient
				fa.save()

			email_body = '''An Ariento guest, %s, has sent you a file.\nClick here to download it:http://ec2-54-172-241-8.compute-1.amazonaws.com/download/%s/\nMessage:%s''' % (sender, str(af.id), message)
			emailer.sendmail(recipient, "Ariento File Send", email_body)

			context = {
				'recipient': recipient,
				'num_files': len(attachment),
			}
			template = loader.get_template('success.html')
			return HttpResponse(template.render(context, request))

def login(request):
	if 'authorized_user' in request.session:
		return redirect('/client')
	else:
		return render(request, 'login.html', {})

def logout(request):
        if 'authorized_user' in request.session:
                del request.session['authorized_user']
                request.session.flush()
                res = redirect('index.html')
                res.delete_cookie('csrftoken')
                return res
        else:
            return redirect('index.html')

def refclient(request):
        if 'authorized_user' in request.session:
                email = request.session['authorized_user']
                try:
                        user = User.objects.get(email=email)
                except ObjectDoesNotExist:
                        del request.session['authorized_user']
                        return render(request, 'login.html', {})
        else:
                try:
                        email = request.POST['login']
                        # TODO: SafeNet authentication
                        password = request.POST['password']
                except KeyError:
                        return render(request, 'login.html', {})

                try:
                        user = User.objects.get(email=email)
                except ObjectDoesNotExist:
                        return render(request, 'login.html', {})
                else:
                        request.session['authorized_user'] = email

        inbox_list = FileAccess.objects.filter(recipient_email=user.email)
        outbox_list = FileAccess.objects.filter(sender_email=user.email)
        user_email = user.email
        context = {
                'inbox_list': inbox_list,
                'outbox_list': outbox_list,
                'user_email' : user_email,
        }

        data = {}                    
        data['inbox'] = render_to_string('refclientin.html', context,request=request)
        data['outbox'] = render_to_string('refclientout.html', context,request=request)
        pl = json.dumps(data)
        return HttpResponse(pl, content_type="application/json")

def user_download(request):
	try:
		key = request.POST['key']
		email = request.session['authorized_user']
	except KeyError:
		return response_file_not_found(request)
	try:
		arientoFile = ArientoFile.objects.get(id=key)
		access = FileAccess.objects.get(file=arientoFile)
		user = User.objects.get(email=email)
	except ObjectDoesNotExist:
		return response_file_not_found(request)
	else:
		if (user.email != access.recipient_email and user.email != access.sender_email):
			return response_file_not_found(request)
		if (access.file_expiration_date <= timezone.now() or access.download_count >= access.download_limit):
			arientoFile.delete()
			return response_file_not_found(request)
		else:
			# increase download count
			access.download_count = access.download_count + 1
			access.save()

			response = HttpResponse(content_type='application/octet-stream')
			response['Content-Disposition'] = 'attachment; filename='+arientoFile.file.name
			response.write(arientoFile.file.read())
			return response
