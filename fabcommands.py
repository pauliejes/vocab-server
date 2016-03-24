import os
import sys
from fabric.api import local

def setup_env():
    INSTALL_STEPS = ['virtualenv ../env;. ../env/bin/activate;pip install -r requirements.txt;deactivate']
    for step in INSTALL_STEPS:
        local(step)

def setup_project():
    # Add env packages and project to the path
    cwd = os.path.dirname(os.path.abspath(__file__))
    if not cwd in sys.path:
        sys.path.append(cwd)

    env_dir = os.path.join(cwd, '../env/lib/python2.7/site-packages')
    if not env_dir in sys.path:
        sys.path.append(env_dir)

    log_dir = os.path.join(cwd, '../logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    celery_log_dir = os.path.join(log_dir, 'celery')
    if not os.path.exists(celery_log_dir):
        os.makedirs(celery_log_dir)

    supervisord_log_dir = os.path.join(log_dir, 'supervisord')
    if not os.path.exists(supervisord_log_dir):
        os.makedirs(supervisord_log_dir)

    local('./VOCAB_SITE/manage.py makemigrations vocab')
    local('./VOCAB_SITE/manage.py migrate')
    local('./VOCAB_SITE/manage.py createsuperuser')
    local('./VOCAB_SITE/manage.py loaddata initial.json')

    # Add settings module so fab file can see it
    os.environ['DJANGO_SETTINGS_MODULE'] = "vocab_site.settings"