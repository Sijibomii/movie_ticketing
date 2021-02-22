from django.core.asgi import get_asgi_application
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter 
from seats.consumers import SeatsConsumer
from .middleware import TokenAuthMiddlewareStack
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': TokenAuthMiddlewareStack( 
        URLRouter([
            path('movie/', SeatsConsumer.as_asgi()),
        ])
    ),
})