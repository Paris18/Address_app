
# Django Imports
from rest_framework import serializers

# project level imports
from accounts.users.models import User



def get_executive_object(mobile):
	try:
		return User.objects.get(mobile=mobile)
	except:
		raise serializers.ValidationError('Authorization error')


def get_executive_id(mobile):
	try:
		print (mobile.employee_id,type(mobile),"\n\n\n\n\n")
		data = User.objects.get(mobile=mobile)
		return User.objects.get(mobile=mobile).employee_id
	except:
		raise serializers.ValidationError('Authorization error')
