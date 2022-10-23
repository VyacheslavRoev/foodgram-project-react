#!/bin/bash

gunicorn --bind :8000 dockerdjango.wsgi:application