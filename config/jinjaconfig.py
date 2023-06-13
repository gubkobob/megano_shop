from jinja2 import Environment
from django.contrib import messages

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'get_messages': messages.get_messages,
        })
    return env
