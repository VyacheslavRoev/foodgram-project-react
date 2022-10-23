#!/bin/bash

gunicorn --bind :8000 --workers=5 --threads=2 dockerdjango.wsgi:application
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput