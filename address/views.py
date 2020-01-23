# django imports
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate


# app level imports
from .serializers import (
	AddressCreateSerializer,
	ListAddressSerializer,
	UpdateAddressSerializer,
)
from .services import (
		AddressSevice,
	)

# project level imports
from libs.constants import (
		BAD_REQUEST,
		BAD_ACTION,
		OPERATION_NOT_ALLOWED,
)
from libs.exceptions import (
							ParseException,
							ResourceNotFoundException,
							)


class AddressViewSet(GenericViewSet):
	"""
	"""
	permission_classes = [IsAuthenticated, ]
	http_method_names = ['get', 'post', 'put', 'delete']

	def get_queryset(self,user,filterdata=None):
		self.queryset = AddressSevice.get_queryset(user)
		if filterdata:
			self.queryset = self.queryset.filter(**filterdata)
		return self.queryset

	serializers_dict = {
		'add_address': AddressCreateSerializer,
		'list_address': ListAddressSerializer,
		'delete_address': ListAddressSerializer,
		'update_address': UpdateAddressSerializer,
	}

	def get_serializer_class(self):
		"""
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)

	@action(methods=['post'], detail=False,)
	def add_address(self, request):
		""" adding Address controler"""
		try:
			data = request.data
			data["user"] = request.user.id
			serializer = self.get_serializer(data=data)
			if serializer.is_valid() is False:
				raise ParseException(BAD_REQUEST, serializer.errors)

			user = serializer.save()
			if user:
				return Response({'status':'address Created Successfully'}, status=status.HTTP_201_CREATED) 

			return Response({'status':'Failed', 'result':None},status=status.HTTP_400_BAD_REQUEST) 
		except Exception as e:
			raise ParseException(BAD_REQUEST, serializer.errors)


	@action(methods=['get'], detail=False,)
	def list_address(self, request):
		"""
		list all my address.
		"""
		try:
			data = self.get_queryset(request.user.id)
			page = self.paginate_queryset(data)
			serialiser = self.get_serializer(page,many=True)
			return self.get_paginated_response(serialiser.data)

		except Exception as e:
			raise ParseException(BAD_REQUEST, serializer.errors)

	@action(methods=['delete'], detail=False,)
	def delete_address(self, request):
		"""
		Delete the address of given id.
		"""
		try:
			address_id = request.GET.get('id')
			data = AddressSevice.get_instance(request.user.id,address_id)
			data.delete()
			return Response(({"detail": "deleted successfully."}),
				status=status.HTTP_200_OK)
		except Exception as e:
			return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)

	@action(methods=['put'], detail=False,)
	def update_address(self, request):
		"""
		update the address.
		"""
		try:

			objects = AddressSevice.get_instance(request.user.id,request.data["id"])
			serializer = self.get_serializer(objects, data=request.data)
			if serializer.is_valid() is False:
				raise ParseException(BAD_REQUEST, serializer.errors)

			user = serializer.save()
			if user:
				return Response({'detail':'updated successfully'},status=status.HTTP_200_OK)
			
			return Response({'status':'Failed', 'result':None},status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			print(str(e))
			raise ParseException(BAD_REQUEST, serializer.errors)