from jinja2 import Environment
from app_catalog.models import Category
from django.contrib import messages

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'get_messages': messages.get_messages,
        'categories': Category.objects.all()
        })
    return env
