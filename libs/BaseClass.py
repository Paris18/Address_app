# Django import
from django.db import models

#app level imports
from accounts.users.models import (
		User,
)

class CreatedUpdatedModel(models.Model):
	"""
		CreatedUpdatedModel is an abstract model to add following fields in every
		model where it is inherited.
			- created_by
			- updated_by
	"""		
	created_by = models.ForeignKey(
							User,
							on_delete=models.PROTECT,
							blank=True, 
							null=True,
							limit_choices_to={'is_vendor': True},
					)
	updated_by = models.ForeignKey(
							User,
							on_delete=models.PROTECT,
							blank=True,
						  null=True,
						  related_name='%(class)s_requests_created',
							limit_choices_to={'is_vendor': True},
					)

	class Meta:
		abstract = True

