# """
# ASGI config for Cashierless project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
# """

# import os

# from django.core.asgi import get_asgi_application
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Cashierless.settings')
# application = get_asgi_application()

import os

from django.core.asgi import get_asgi_application
from .websockets import websocket_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Cashierless.settings')

django_application = get_asgi_application()

async def application(scope, receive, send):
    if scope['type'] == 'http':
        await django_application(scope, receive, send)
    elif scope['type'] == 'websocket':
        await websocket_application(scope, receive, send)
    else:
        raise NotImplementedError(f"Unknown scope type {scope['type']}")