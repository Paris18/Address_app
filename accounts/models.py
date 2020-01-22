
# python imports
import uuid


# django/rest_framwork imports
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.validators import UniqueValidator
# from django.contrib.postgres.fields import JSONField

# project level imports
# from libs.models import TimeStampedModel
# from libs.clients import sms_client
# from libs.utils.otp import create_otp

# app level imports
# from .managers import UserManager
# from accounts.constants import TOO_MANY_ATTEMPTS, INVALID_OTP

# third party imports
from model_utils import Choices
# from jsonfield import JSONField

# class ProfileManager(models.Manager):
# 	pass

class Profile(models.Model):
	GENDER = Choices(
		('M', 'Male'),
		('F', 'Female'),
		('O', 'Other'),
	)

	user = models.OneToOneField(
		User,
		on_delete=models.CASCADE,
		)

	mobile = models.IntegerField(
		blank = True,
		unique=True,
		)

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	gender = models.CharField(choices=GENDER, max_length=1, blank=True)
	image_url = models.CharField(max_length=255, blank=True)

	# objects = ProfileManager()



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	print(instance.mobile)
	if created:
		Profile.objects.create(user=instance,mobile=instance.mobile)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()
