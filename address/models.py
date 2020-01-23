# python imports
import uuid

# Django Imports
from django.db import models
from django.contrib.auth.models import User

# app level imports
from libs.models import TimeStampedModel


class Address(TimeStampedModel):
    """
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=65, blank=False)
    address = models.TextField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user'
    )
