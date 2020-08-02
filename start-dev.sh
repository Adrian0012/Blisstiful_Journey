#!/bin/bash
export PROTOCOL=https
# export SITE_NAME=localhost
export SITE_NAME=051f1b16b833.ngrok.io

DJANGO_SETTINGS_MODULE=bliss_blog.settings ~/environment/bliss_blog_env/bin/python manage.py runserver
