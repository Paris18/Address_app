# Django imports
from django.contrib.auth import backends
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken

# App level imports
from .models import Profile


# Project level imports
from libs.exceptions import (
							ParseException,
							ResourceNotFoundException,
							)

class AuthenticationBackend(backends.ModelBackend):
	"""
	Custom authentication Backend for login using email,phone,username 
	with password
	"""
	def authenticate(self, username=None,mobile = None,email = None, password=None, **kwargs):
		""" custom authenticate with mobile or email"""
		try:
			user = Profile.objects.get(
				Q(mobile=mobile) | Q(user__email__iexact=email))
			if user.user.check_password(password):
				return user.user
		except Profile.DoesNotExist:
			pass


class JWTtoken:
	""" jwt creating using the user instance"""

	@staticmethod
	def get_tokens_for_user(user):
	    refresh = RefreshToken.for_user(user)

	    return {
	        'refresh': str(refresh),
	        'access': str(refresh.access_token),
	    }


class UserService:

	@classmethod
	def get_queryset(cls, filter_data = None):
		"""
		fetching the user queryset on user id
		"""
		queryset = User.objects.all()
		if filter_data:
			try:
				queryset = queryset.filter(**filter_data)
			except:
				raise ParseException(BAD_REQUEST)
		return queryset
		
	@classmethod
	def get_instance(cls,user_id):
		"""
		fetching the user instance on user id
		"""
		try:
			return User.objects.get(id=user_id)
		except User.DoesNotExist:
			raise ResourceNotFoundException(BAD_REQUEST)


class ProfileSevice:

	@classmethod
	def get_queryset(cls, filter_data = None):
		"""
		fetching the profile queryset on profile id
		"""
		queryset = Profile.objects.select_related('user').all()
		if filter_data:
			try:
				queryset = queryset.filter(**filter_data)
			except:
				raise ParseException(BAD_REQUEST)
		return queryset
		
	@classmethod
	def get_instance(cls,user):
		"""
		fetching the profile instance on profile id
		"""
		try:
			return Profile.objects.select_related('user').get(user=user)
		except Profile.DoesNotExist:
			raise ResourceNotFoundException(BAD_REQUEST)


		