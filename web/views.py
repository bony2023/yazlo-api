from django.shortcuts import render
import requests, json
from django.http import JsonResponse, Http404
from django.conf import settings
from api.api_views.db_helper import *
from functions import *
import datetime, os

def index(request):
	return render(request, 'web/index.html')

def verifycaptcha(request):
	if request.is_ajax():
		verifyUrl = 'https://www.google.com/recaptcha/api/siteverify'
		params = {
			"secret": os.getenv('RECAPTCHA_SECRET'),
			"response": request.GET.get('response', None)
		}
		response = requests.request("POST", verifyUrl, params=params)
		if response:
			response = json.loads(response.text)
			if response.get('success') == "true" or response.get('success') == True:
				if not registerUser(request.GET.get("email")):
					response['success'] = False
		return JsonResponse(response)

def registerUser(email):
	db = getDatabase()
	if db and not (db.users.find_one({"email": email}) or db.registerUser.find_one({"email": email})):
		userToken = getRandomToken(28)
		dateCreated = datetime.datetime.utcnow()
		db.registerUser.insert_one({
			"email": email,
			"register_token": userToken,
			"date_created": dateCreated
		})
		if sendUserMail(email, userToken) == 1:
			return True
	return False

def sendUserMail(email, userToken):
	params = {
		'receiver': email,
		'activationLink': '{}/verifyuser/{}'.format(settings.HOSTNAME, userToken)
	}
	subject = 'Acivate your account'
	to = email
	htmlFile = 'email/activate.html'
	return send_mail(subject = subject, to = to, htmlFile = htmlFile, params = params)

def verifyuser(request, token):
	db = getDatabase()
	if db:
		registered_user = db.registerUser.find_one({"register_token": token})
		if registered_user:
			user_application_id = getRandomToken(10)
			user_application_secret = getRandomToken(35)
			db.users.insert_one({
				"email": registered_user["email"],
				"application_id": user_application_id,
				"application_secret": user_application_secret
			})
			if sendActivationMail(registered_user["email"], user_application_id, user_application_secret) == 1:
				db.registerUser.delete_one({"email": registered_user["email"]})
				return JsonResponse({'success': True, 'message': 'Check your email for API credentials.'})
	raise Http404

def sendActivationMail(email, application_id, application_secret):
	params = {
		'receiver': email,
		'app_id': application_id,
		'app_secret': application_secret
	}
	subject = 'API Credentials'
	to = email
	htmlFile = 'email/api_credentials.html'
	return send_mail(subject = subject, to = to, htmlFile = htmlFile, params = params)