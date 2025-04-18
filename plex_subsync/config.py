import os

# Plex and Home Assistant configuration
PLEX_URL = os.getenv("PLEX_URL")
PLEX_TOKEN = os.getenv("PLEX_TOKEN")
HOME_ASSISTANT_WEBHOOK_URL = os.getenv("HOME_ASSISTANT_WEBHOOK_URL")

# Local library directory mount point
PLEX_LIBRARY_DIR = "/media"

# Notification message templates
# Notification message templates
NOTIFICATION_MESSAGE_TEMPLATE = "SubSync finished for: {}"
START_MESSAGE_TEMPLATE = "SubSync started for: {}"
# failure template for failure notifications, includes error cause
FAILURE_MESSAGE_TEMPLATE = "SubSync failed for: {}. Reason: {}"

# Default language codes (ISO-639-1); can be overridden via environment variables
DEFAULT_AUDIO_LANG = os.getenv("DEFAULT_AUDIO_LANG", "en")
DEFAULT_SUB_LANG = os.getenv("DEFAULT_SUB_LANG", "en")