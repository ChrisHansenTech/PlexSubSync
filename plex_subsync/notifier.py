"""
Home Assistant notification functions.
"""
import requests
from .config import HOME_ASSISTANT_WEBHOOK_URL

def send_home_assistant_notification(message: str):
    """Send a notification via the Home Assistant webhook."""
    try:
        response = requests.post(HOME_ASSISTANT_WEBHOOK_URL, json={"message": message})
        response.raise_for_status()
        print("Home Assistant webhook sent successfully.")
    except requests.RequestException as e:
        print(f"Failed to send Home Assistant webhook: {e}")