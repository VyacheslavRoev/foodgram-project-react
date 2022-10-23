#!/bin/bash

gunicorn --bind :8000 --workers=5 --threads=2 dockerdjango.wsgi:application