#!/bin/bash
export PROTOCOL=https
# export SITE_NAME=localhost
export SITE_NAME=58454e328d5a.ngrok.io

DJANGO_SETTINGS_MODULE=bliss_blog.settings ~/environment/bliss_blog_env/bin/python manage.py runserver
