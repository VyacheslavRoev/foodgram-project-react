#!/bin/bash

python manage.py collectstatic --noinput && python manage.py migrate
gunicorn --bind :8000 --workers=5 --threads=2 dockerdjango.wsgi:application