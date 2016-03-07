from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

class RegisteredIRI(models.Model):
	address = models.URLField(unique=True)
	userprofile = models.ForeignKey(UserProfile, null=True)