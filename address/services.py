# app level imports
from .models import Address


# Project level imports
from libs.exceptions import (
							ParseException,
							ResourceNotFoundException,
							)

class AddressSevice:

	@classmethod
	def get_queryset(cls,user, filter_data = None):
		"""
		fetching the profile queryset on profile id
		"""
		queryset = Address.objects.select_related('user').filter(user=user)
		if filter_data:
			try:
				queryset = queryset.filter(**filter_data)
			except:
				raise ParseException(BAD_REQUEST)
		return queryset
		
	@classmethod
	def get_instance(cls,user,address_id):
		"""
		fetching the profile instance on profile id
		"""
		try:
			return Address.objects.select_related('user').get(user=user,id=address_id)
		except Address.DoesNotExist:
			raise ResourceNotFoundException(BAD_REQUEST)


		