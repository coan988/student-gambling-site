from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def send_points_update(user_id: int, points: int):
    """
    Sendet ein Live-Update über Channels an den WebSocket des Nutzers.
    Falls Redis nicht verfügbar ist, wird nichts getan (fail silently).
    """
    try:
        layer = get_channel_layer()
        if layer is not None:
            async_to_sync(layer.group_send)(
                f"user_{user_id}",
                {
                    "type": "points_update",
                    "points": points
                }
            )
    except Exception:
        # Redis nicht verfügbar - das ist OK, einfach überspringen
        # Die App funktioniert trotzdem, nur ohne Live-Updates
        pass