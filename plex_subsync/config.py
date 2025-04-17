import os

# Plex and Home Assistant configuration
PLEX_URL = os.getenv("PLEX_URL")
PLEX_TOKEN = os.getenv("PLEX_TOKEN")
HOME_ASSISTANT_WEBHOOK_URL = os.getenv("HOME_ASSISTANT_WEBHOOK_URL")

# Local library directory mount point
PLEX_LIBRARY_DIR = "/media"

# Notification message templates
NOTIFICATION_MESSAGE_TEMPLATE = "SubSync finished for: {}"
START_MESSAGE_TEMPLATE = "SubSync started for: {}"
FAILURE_MESSAGE_TEMPLATE = "SubSync failed for: {}"