"""
Home Assistant notification functions.
"""
import requests
from .config import HOME_ASSISTANT_WEBHOOK_URL

def send_home_assistant_notification(stage: str, message: str, media_id: int, entity_id: str):
    """Send a notification via the Home Assistant webhook."""
    try:
        response = requests.post(HOME_ASSISTANT_WEBHOOK_URL, json={ "stage": stage, "message": message, "media_id": media_id, "entity_id": entity_id })
        response.raise_for_status()
        print("Home Assistant webhook sent successfully.", flush=True)
    except requests.RequestException as e:
        print(f"Failed to send Home Assistant webhook: {e}", flush=True)