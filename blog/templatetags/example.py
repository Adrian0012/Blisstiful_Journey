#name of the file must be example.py

from django import template
import readtime

register = template.Library()

def read(html):
    result = readtime.of_html(html)
    return result.text

register.filter('readtime',read)