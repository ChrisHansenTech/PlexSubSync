import os

# Plex and Home Assistant configuration
PLEX_URL = os.getenv("PLEX_URL")
PLEX_TOKEN = os.getenv("PLEX_TOKEN")
HOME_ASSISTANT_WEBHOOK_URL = os.getenv("HOME_ASSISTANT_WEBHOOK_URL")

# Local library directory mount point (container mount). Can be overridden via environment variable.
PLEX_LIBRARY_DIR = os.getenv("PLEX_LIBRARY_DIR", "/media")
# Prefix of Plex API returned file paths to strip when mapping to container path.
# Example: "\\server\share\plex\movies" or "/mnt/plexdrive/movies".
PLEX_API_PATH_PREFIX = os.getenv("PLEX_API_PATH_PREFIX", "")

# Notification message templates
NOTIFICATION_MESSAGE_TEMPLATE = "SubSync finished for: {}"
START_MESSAGE_TEMPLATE = "SubSync started for: {}"

# Failure template for failure notifications, includes error cause
FAILURE_MESSAGE_TEMPLATE = "SubSync failed for: {}. Reason: {}"

# Sync stage
STAGE_SYNC_START = "sync-started"
STAGE_SYNC_FINISHED = "sync-success"
STAGE_SYNC_FAILED = "sync-failed"

# Default language codes (ISO-639-1); can be overridden via environment variables
DEFAULT_AUDIO_LANG = os.getenv("DEFAULT_AUDIO_LANG", "en")
DEFAULT_SUB_LANG = os.getenv("DEFAULT_SUB_LANG", "en")