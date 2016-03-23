from __future__ import unicode_literals

import json

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models, IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver

from .tasks import notify_admins

TERM_TYPE_CHOICES = (
	('', ''),
	('verbs', 'Verbs'),
	('activityTypes', 'Activity Types'),
	('attachments', 'Attachments'),
	('extensions', 'Extensions')
)

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def __unicode__(self):
		return json.dumps({"user": self.user.username, "registeredIRIs": [iri.return_address() for iri in self.registerediri_set.all()]})

class RegisteredIRI(models.Model):
	vocabulary_path = models.CharField(max_length=50)
	term_type = models.CharField(max_length=15, blank=True, choices=TERM_TYPE_CHOICES)
	term = models.CharField(max_length=50, blank=True)
	accepted = models.BooleanField(default=False)
	reviewed = models.BooleanField(default=False)
	userprofile = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL)

	def return_address(self):
		if self.term_type:
			if self.term:
				return settings.IRI_DOMAIN + "/".join([self.vocabulary_path, self.term_type, self.term])
			return settings.IRI_DOMAIN + "/".join([self.vocabulary_path, self.term_type])
		return settings.IRI_DOMAIN + self.vocabulary_path

	class Meta:
		unique_together = ("vocabulary_path", "term_type", "term")

	def save(self, *args, **kwargs):
		if self.term and not self.term_type:
			raise IntegrityError("Must supply a term type if supplying a term")
		super(RegisteredIRI, self).save(*args, **kwargs)

	def __unicode__(self):
		return json.dumps({"address": self.return_address(), "user": self.userprofile.user.username})

@receiver(post_save, sender=RegisteredIRI)
def iri_post_save(sender, **kwargs):
	if kwargs['created']:
		notify_admins.delay(kwargs['instance'].return_address())

class VocabularyData(models.Model):
	name = models.CharField(max_length=250)
	iri = models.OneToOneField(RegisteredIRI, blank=True, null=True, on_delete=models.SET_NULL)
	user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
	editorialNote = models.TextField()
	# what about copName, copUrl, dateCreated, dateModified, revisionNum, numTerms

	def __unicode__(self):
		return "%s:%s" % (self.id, self.name)

class Term(models.Model):
	name = models.CharField(max_length=250)
	vocabulary = models.ForeignKey(Vocabulary)

	def __unicode__(self):
		return "%s:%s" % (self.id, self.name)
