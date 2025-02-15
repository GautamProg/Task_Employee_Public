"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import employee_management.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup() # new line added for websockets

# application = get_asgi_application()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(employee_management.routing.websocket_urlpatterns),
})

