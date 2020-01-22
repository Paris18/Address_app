# python imports
import logging
import datetime

# django level imports
from django.core.mail import EmailMessage,send_mail

# project imports
# from dinsanti.settings import EMAIL_HOST_USER

EMAIL_HOST_USER = "pariskamal8@gmail.com"


logger = logging.getLogger(__name__)

def sendmail(message,subject,tolist):
	try:
		# msg = EmailMessage(subject, message, EMAIL_HOST_USER, tolist) 
		# msg.send(fail_silently=True)
		send_mail(subject, message, EMAIL_HOST_USER, tolist)
		logger.info("Mail Sent ")
		return 1
	except:
		print ("Here we are 2")
		logger.error("Sending mail is failed", exc_info=True)
		return 0




