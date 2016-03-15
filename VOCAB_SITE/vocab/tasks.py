from __future__ import absolute_import

from celery import shared_task
from celery.utils.log import get_task_logger

from django.core import mail
from django.core.mail import mail_admins, send_mail

celery_logger = get_task_logger('celery-task')

@shared_task
def notify_user(iri, email, result):
    try:
        with mail.get_connection():
            send_mail("Your xAPI vocabulary IRI has been processed", ("Your IRI, %s, has been %s.\n"
                "If it was rejected we most likely found the IRI already created in a different repository.\n"
                "Please email helpdesk@adlnet.gov if you have any questions.") % (iri, "accepted" if result == True else "rejected"), \
                "adlvocab@gmail.com", [email], fail_silently=False)
    except Exception, e:
        celery_logger.exception("Email IRI owner error: " + e.message)

@shared_task
def notify_admins(iri):
    try:
        with mail.get_connection():
            mail_admins("New IRI Alert", "There is a new IRI (%s) waiting for you to review." % iri, fail_silently=False)    
    except Exception, e:
        celery_logger.exception("Email admins error: " + e.message)        