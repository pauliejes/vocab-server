# vocab-server

## Installation

**Install Prerequisites**

    admin:~$ sudo apt-get install git fabric postgresql python-setuptools postgresql-server-dev-all python-dev rabbitmq-server
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

**Setup RabbitMQ**
   
   ```
   admin:~$ sudo rabbitmqctl add_user <username_for_rabbitmq> <password_for_rabbitmq>
   admin:~$ sudo rabbitmqctl add_vhost <vhost_name>
   admin:~$ sudo rabbitmqctl set_permissions -p <vhost_name> <username_for_rabbitmq> ".*" ".*" ".*"
   ```

**Setup Celery**

***Configure vocab/celery.py***

    app = Celery('vocab',
			broker='amqp://<username_for_rabbitmq>:<password_for_rabbitmq>@localhost:5672/<vhost_name>',
			include=['vocab.tasks'])

***Configure VOCAB_SITE/celeryd.conf***

   ```
   command=/path/to/vocab_container/env/bin/celery worker -A vocab --loglevel=DEBUG
   directory=/path/to/vocab_container/vocab-server/VOCAB_SITE
   stdout_logfile=/path/to/vocab_container/logs/celery/outworker.log
   stderr_logfile=/path/to/vocab_container/logs/celery/errworker.log
   ```

***Configure VOCAB_SITE/supervisord.conf***

   ```
   logfile=/path/to/vocab_container/logs/supervisord/supervisord.log
   childlogdir=/path/to/vocab_container/logs/supervisord/
   ```

***Create upstart script in `/etc/init` named vocab-email.conf***

   ```
   description    "supervisor for vocab-email"
   start on runlevel    [2345]
   stop on runlevel    [!2345]

   respawn

   setuid <your system username>
   chdir /path/to/vocab_container/vocab-server/VOCAB_SITE
   exec /path/to/vocab_container/env/bin/supervisord --nodaemon
   ```

Control celery tasks with: `sudo {start|stop|restart} vocab-email`. Every change done to any file involving celery (including tasks.py), requires a restart of the celery service.

## Starting

While in the VOCAB_SITE directory, run

    (env)admin:$ python manage.py runserver


