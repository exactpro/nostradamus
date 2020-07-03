from channels.routing import ProtocolTypeRouter, URLRouter
import apps.extractor.routing
from nostradamus.token_middleware import JWTAuthMiddlewareStack

application = ProtocolTypeRouter(
    {
        "websocket": JWTAuthMiddlewareStack(
            URLRouter(apps.extractor.routing.websocket_urlpatterns),
        )
    }
)
