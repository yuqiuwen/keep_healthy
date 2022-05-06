"""
ASGI config for keep_healthy project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from . import routings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dream_world.settings')

# application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),                             # urls.py views.py
    "websocket": URLRouter(routings.webscoket_urlpatterns),     # routings.py consumers.py
})
