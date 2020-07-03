from django.urls import path

from apps.extractor.consumers import ExtractorConsumer

websocket_urlpatterns = [path("extractor_listener/", ExtractorConsumer)]
