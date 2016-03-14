from __future__ import absolute_import

from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
from celery.utils.log import get_task_logger

from django.db import transaction


celery_logger = get_task_logger('celery-task')

@shared_task
@transaction.atomic
def void_statements(stmts):
    pass