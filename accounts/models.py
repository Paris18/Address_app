
# python imports
import uuid,os


# django/rest_framwork imports
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.validators import UniqueValidator
from django.conf import settings


# app level imports
from libs.models import TimeStampedModel

# third party imports
from model_utils import Choices


def profile_path(instance, filename): 
  
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    extension = filename.split('.')[-1]
    image_name = 'user_{0}/{0}.{1}'.format(instance.user.id, extension)
    fullname = os.path.join(settings.MEDIA_ROOT, image_name)
    if os.path.exists(fullname):
        os.remove(fullname) 
    return fullname 


class Profile(TimeStampedModel):
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
	profile_image = models.ImageField(upload_to = profile_path) 




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance,mobile=instance.mobile)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()
