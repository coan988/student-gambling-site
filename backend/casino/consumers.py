from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync

class PointsConsumer(JsonWebsocketConsumer):
    def connect(self):
        user = self.scope["user"]
        if user.is_anonymous:
            self.close(); return
        self.group_name = f"user_{user.id}"
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()
        self.send_json({"type": "points_update", "points": user.points})

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)

    def points_update(self, event):
        self.send_json({"type": "points_update", "points": event["points"]})