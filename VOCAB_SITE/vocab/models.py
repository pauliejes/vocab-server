from __future__ import unicode_literals

import json

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core import mail
from django.core.mail import mail_admins, send_mail
from django.db import models, IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def __unicode__(self):
		return json.dumps({"user": self.user.username, "registeredIRIs": [iri.return_address() for iri in self.registerediri_set.all()]})	

class RegisteredIRI(models.Model):
	vocabulary = models.CharField(max_length=50)
	term_type = models.CharField(max_length=50, blank=True, null=True)
	term = models.CharField(max_length=50, blank=True, null=True)
	accepted = models.BooleanField(default=False)
	reviewed = models.BooleanField(default=False)
	userprofile = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL)

	def return_address(self):
		if self.term_type:
			if self.term:
				return settings.IRI_DOMAIN + "/".join([self.vocabulary, self.term_type, self.term])
			return settings.IRI_DOMAIN + "/".join([self.vocabulary, self.term_type])
		return settings.IRI_DOMAIN + self.vocabulary

	class Meta:
		unique_together = ("vocabulary", "term_type", "term")

	def save(self, *args, **kwargs):
		if self.term and not self.term_type:
			raise IntegrityError("Must supply a term type if supplying a term")
		super(RegisteredIRI, self).save(*args, **kwargs)

	def __unicode__(self):
		return json.dumps({"address": self.return_address(), "user": self.userprofile.user.username})

@receiver(post_save, sender=RegisteredIRI)
def iri_post_save(sender, **kwargs):
	if kwargs['created']:
		with mail.get_connection() as connection:
			mail_admins("New IRI Alert", "There is a new IRI waiting for you to review.", fail_silently=False)