from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def send_points_update(user_id: int, points: int):
    """
    Sendet ein Live-Update über Channels an den WebSocket des Nutzers.
    """
    layer = get_channel_layer()
    async_to_sync(layer.group_send)(
        f"user_{user_id}",
        {
            "type": "points_update",
            "points": points
        }
    )