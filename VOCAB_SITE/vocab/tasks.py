from __future__ import absolute_import

import fcntl

from celery import shared_task
from celery.utils.log import get_task_logger

from django.conf import settings
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

@shared_task
def update_htaccess(title, vocab, json_redirect, html_redirect): 
    from .models import RegisteredIRI
    vocab_already_registered = RegisteredIRI.objects.filter(vocabulary=vocab, accepted=True, reviewed=True)

    if not vocab_already_registered:
        unwritten = True
        tries = 0
        while(unwritten and tries < 10):
            try:
                with open('test.txt', 'a') as htaccess:
                    fcntl.flock(htaccess, fcntl.LOCK_EX)
                    content = settings.HTACCESS_SECTION_TEMPLATE.replace("OURTITLEREPLACEMENT", title).replace("OURVOCABREPLACEMENT", vocab) \
                        .replace("OURJSONLDREDIRECTREPLACEMENT", json_redirect).replace("OURHTMLREDIRECTREPLACEMENT", html_redirect)
                    htaccess.write(content)
                    fcntl.flock(htaccess, fcntl.LOCK_UN)
                    unwritten = False
            except IOError, ioe:
                celery_logger.exception("htaccess file was locked, trying again....")
                tries += 1
            except Exception, e:
                with mail.get_connection():
                    mail_admins("HTACCESS File Edit Error", "Content with vocab %s was not written to htaccess. Please fix immediately." % \
                    (vocab), fail_silently=False)
                unwritten = False