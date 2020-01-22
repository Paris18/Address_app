from django.contrib.auth import backends
from accounts.models import Profile
from django.db.models import Q

class AuthenticationBackend(backends.ModelBackend):
	"""
	Custom authentication Backend for login using email,phone,username 
	with password
	"""
	def authenticate(self, username=None,mobile = None,email = None, password=None, **kwargs):
		try:
			print (mobile,email,password)
			user = Profile.objects.get(
				Q(mobile=mobile) | Q(user__email__iexact=email))
			if user.user.check_password(password):
				return user.user
		except Profile.DoesNotExist:
			pass