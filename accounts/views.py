# django imports
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
# from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
# from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


# app level imports
from .models import (
					Profile,
					)

from .serilaizers import (
	UserLoginRequestSerializer,
	UserRegSerializer,
	UserListSerializer,
	UserUpdateRequestSerializer,
	ProfileListSerializer,
	ProfileUpdateSerializer,
)
from .services import (
		JWTtoken,
		UserService,
		ProfileSevice,
	)

# project level imports
from libs.constants import (
		BAD_REQUEST,
		BAD_ACTION,
		OPERATION_NOT_ALLOWED,
)
# from accounts.constants import COULD_NOT_SEND_OTP, USER_NOT_REGISTERED
from libs.exceptions import (
							ParseException,
							ResourceNotFoundException,
							)

from libs import (
				# redis_client,
				ganeratepass,
				mail,
				)



class UserViewSet(GenericViewSet):
	"""
	"""

	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	def get_queryset(self):
		return UserService.get_queryset()

	serializers_dict = {
		'login': UserLoginRequestSerializer,
		'register': UserRegSerializer,
		'admin': UserListSerializer,
		'adminlist':UserListSerializer,
		'admin_update': UserUpdateRequestSerializer,
		# 'list': UserListSerializer,
	}

	def get_serializer_class(self):
		"""
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)

	@action(methods=['post'], detail=False)
	def register(self, request):
		"""
		"""
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid() is False:
			print (serializer.errors)
			raise ParseException(BAD_REQUEST, serializer.errors)
	

		print("registering user with", serializer.validated_data)

		user = serializer.save()
		if user:
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response({}, status.HTTP_200_OK)

	@action(methods=['post'], detail=False)
	def login(self, request):

		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid() is False:
			raise ParseException(BAD_REQUEST, serializer.errors)

		print (serializer.validated_data["password"])
		mobile = serializer.validated_data.get("mobile",None)
		email = serializer.validated_data.get("email",None)

		user = authenticate(
			mobile = mobile,
			email = email,
			password=serializer.validated_data["password"])

		if not user:
			return Response({'error': 'Invalid Credentials'},
							status=status.HTTP_404_NOT_FOUND)

		tokens = JWTtoken.get_tokens_for_user(user)
		return Response(tokens,
						status=status.HTTP_200_OK)

	# @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ])
	# def logout(self, request):

	# 	request.user.auth_token.delete()
	# 	return Response(status=status.HTTP_200_OK)


	@action(
		methods=['get', 'patch'],
		detail=False,
		# url_path='image-upload',
		permission_classes=[IsAuthenticated, ],
	)
	def admin(self, request):
		"""
		Return user profile data and groups
		"""
		input_id = request.user.id
		try:
			d = UserService.get_instance(input_id)
			data = self.get_serializer(d).data
			return Response(data, status.HTTP_200_OK)
		except Exception as e:
			raise ResourceNotFoundException(BAD_REQUEST)
			# return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)

	@action(
		methods=['get', 'patch'],
		detail=False,
		# url_path='image-upload',
		permission_classes=[IsAuthenticated, ],
	)
	def adminlist(self, request):
		"""
		Return user profile data and groups
		"""
		try:
			d = self.get_queryset()
			data = self.get_serializer(d,many=True).data
			return Response(data, status.HTTP_200_OK)
		except Exception as e:
			raise ResourceNotFoundException(BAD_REQUEST)

	@action(
		methods=['put'],
		detail=False,
		# url_path='image-upload',
		permission_classes=[IsAuthenticated, ],
	)
	def admin_update(self, request):
		"""
		Return user profile data and groups
		"""
		try:
			data=request.data
			data["id"] = request.user.id
			d = UserService.get_instance(input_id)
			serializer = self.get_serializer(d,data=data)

			if not serializer.is_valid():
				raise ParseException(BAD_REQUEST, serializer.errors)

			serializer.save()
			return Response(serializer.data, status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": str(e)}, status.HTTP_404_NOT_FOUND)




class ProfileViewSet(GenericViewSet):
	"""
	"""

	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	def get_queryset(self):
		return ProfileSevice.get_queryset()

	serializers_dict = {
		'my_profile': ProfileListSerializer,
		'profile_list':ProfileListSerializer,
		'profile_update': ProfileUpdateSerializer,
		# 'list': UserListSerializer,
	}

	def get_serializer_class(self):
		"""
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)

	@action(
		methods=['get', 'patch'],
		detail=False,
		# url_path='image-upload',
		permission_classes=[IsAuthenticated, ],
	)
	def my_profile(self, request):
		"""
		Return user profile data and groups
		"""
		try:
			# print(request.user.email)
			d = ProfileSevice.get_instance(request.user.id)
			data = self.get_serializer(d).data
			return Response(data, status.HTTP_200_OK)
		except Exception as e:
			print(str(e))
			raise ResourceNotFoundException(BAD_REQUEST)
			# return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)

	@action(
		methods=['get', 'patch'],
		detail=False,
		# url_path='image-upload',
		permission_classes=[IsAuthenticated, ],
	)
	def profile_list(self, request):
		"""
		Return user profile data and groups
		"""
		try:
			d = self.get_queryset()
			data = self.get_serializer(d,many=True).data
			return Response(data, status.HTTP_200_OK)
		except Exception as e:
			raise ResourceNotFoundException(BAD_REQUEST)

	@action(
		methods=['put'],
		detail=False,
		# url_path='image-upload',
		permission_classes=[IsAuthenticated, ],
	)
	def profile_update(self, request):
		"""
		Return user profile data and groups
		"""
		try:
			data=request.data
			d = ProfileSevice.get_instance(request.user.id)
			serializer = self.get_serializer(d,data=data)

			if not serializer.is_valid():
				raise ParseException(BAD_REQUEST, serializer.errors)

			serializer.save()
			return Response(serializer.data, status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": str(e)}, status.HTTP_404_NOT_FOUND)

