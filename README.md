# vocab-server

## Installation

**Install Prerequisites**

    admin:~$ sudo apt-get install git fabric postgresql python-setuptools postgresql-server-dev-all python-dev
    admin:~$ sudo easy_install pip
    admin:~$ sudo pip install virtualenv

**Setup Postgres**

    admin:~$ sudo -u postgres createuser -P -s <db_owner_name>
    Enter password for new role: <db_owner_password>
    Enter it again: <db_owner_password>
    admin:~$ sudo -u postgres psql template1
    template1=# CREATE DATABASE vocab OWNER <db_owner_name>;
    template1=# \q (exits shell)

**Clone the repository**

**Set the database configuration**

	### File: VOCAB_SITE/vocab_site/settings.py
	
	# configure the database
	DATABASES = {
    	'default': {
    	    'ENGINE': 'django.db.backends.postgresql',
	        'NAME': 'vocab',
	        'USER': '<db_owner_name>',
	        'PASSWORD': '<db_owner_password>',
	        'HOST': 'localhost',
	        'PORT': '',
	    }
	}

**Setup the environment**

    admin:$ fab -f fabcommands.py setup_env
    admin:$ source ../env/bin/activate
    (env)admin:$

**Setup the project**

    (env)admin:$ fab -f fabcommands.py setup_project
    ...
    You just installed Django's auth system, which means you don't have any superusers defined.
	Would you like to create one now? (yes/no): yes
	Username (leave blank to use '<system_user_name>'): 
	E-mail address:
	Password:
	Password (again): 
	Superuser created successfully.
	...

## Starting

While in the VOCAB_SITE directory, run

    (env)admin:$ python manage.py runserver
