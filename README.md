# TASK-MANAGER-API
## A python django-rest-framework JSON api

# Instructions:

## 1.a. - Requried variables for running the project locally [.env]

DEBUG=1
SECRET_KEY=secret_key
ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
CORS_ORIGIN_ALLOW_ALL=1
EMAIL_HOST_USER=example@email.com
EMAIL_HOST_PASSWORD=email_password

## 1.b. - Example for running the production version:

[.env.prod]:

DEBUG=0
SECRET_KEY=secret_key
ALLOWED_HOSTS=allowed_hosts_here
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=database
SQL_USER=user
SQL_PASSWORD=password
SQL_HOST=sql_host
SQL_PORT=5432
DATABASE=postgres
VIRTUAL_HOST=example-domain.com
VIRTUAL_PORT=8000
LETSENCRYPT_HOST=example-domain.com
CORS_ORIGIN_ALLOW_ALL=0
CORS_ORIGIN_WHITELIST=https://example-domain.com
EMAIL_HOST_USER=example@email.com
EMAIL_HOST_PASSWORD=password

[.env.prod.proxy-companion]:

DEFAULT_EMAIL=example@email.com
NGINX_PROXY_CONTAINER=nginx-proxy

## 2. Create a python virtual env and install dependencies using the commands below:

python3 -m venv env
source env/bin/activate
pip install -r ./task-manager-api/requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

## To run in docker container locally run the commands bellow:

sudo docker-compose up -d



# Before runing the production version:

## Make sure to test using the staging version first because it uses a staging certificate for let's encrypt which does not have a limit on have many times it can be published.

Add this variable to [.env.staging.proxy-companion]:

ACME_CA_URI=https://acme-staging-v02.api.letsencrypt.org/directory