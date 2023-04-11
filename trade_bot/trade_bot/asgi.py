"""
ASGI config for trade_bot project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""



from django.core.asgi import get_asgi_application
import os

from channels.routing import ProtocolTypeRouter,URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from .consumers import BotStatus,LogsChannel
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trade_bot.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Just HTTP for now. (We can add other protocols later.)
    "websocket": URLRouter([
    path('', BotStatus.as_asgi()),
    path('logs/',LogsChannel.as_asgi()),
    ])
})