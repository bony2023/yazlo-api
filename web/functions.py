from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import os

def send_mail(subject, to, htmlFile, params, sender = os.getenv('ADMIN_MAIL')):
	html_content = render_to_string(htmlFile, params)
	text_content = strip_tags(html_content)
	mail = EmailMultiAlternatives(subject, text_content, sender, [to])
	mail.attach_alternative(html_content, "text/html")
	return mail.send()