from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class ExtractorConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            "extractor", self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            "extractor", self.channel_name
        )

    def bugs_updated_event(self, event):
        text = event.get("text", "empty")
        self.send(text_data=text)

    @staticmethod
    def loader_notification():
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "extractor",
            {"type": "bugs_updated_event", "text": "Bugs has been updated"},
        )
