# PlexSubSync

PlexSubSync is a lightweight Python service that receives webhook requests containing Plex media IDs, then uses the Plex API to locate the corresponding media file and subtitle file, and finally syncs the subtitle using [`subsync`](https://github.com/sc0ty/subsync).

This service is designed to work standalone or as part of a larger automation system such as Home Assistant.

## Features

- Accepts webhook requests via HTTP POST
- Looks up video and subtitle paths using the Plex API
- Runs `subsync` to align subtitle timing to the media file
- Sends status updates via optional Home Assistant webhook
- Simple and extendable for media automation workflows

## Requirements

- Python 3.9+
- Plex media server with a valid token
- `subsync` installed and available in your system PATH

## Installation

1. Clone the repository:

```bash
git clone https://github.com/ChrisHansenTech/PlexSubSync.git
cd PlexSubSync
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Install `subsync` (if not already installed):

```bash
pip install subsync
# or follow installation instructions at https://github.com/sc0ty/subsync
```

## Configuration

Set the following environment variables or configure them in a `.env` file:

| Variable           | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| `PLEX_TOKEN`               | Your Plex access token                                               |
| `PLEX_URL`                 | Base URL of your Plex server (e.g., `http://192.168.1.10:32400`)      |
| `HOME_ASSISTANT_WEBHOOK_URL` | (Optional) Home Assistant webhook URL to notify status             |
| `DEFAULT_AUDIO_LANG`         | (Optional) Default ISO-639-1 audio language code if not provided (default: "en") |
| `DEFAULT_SUB_LANG`           | (Optional) Default ISO-639-1 subtitle language code if not provided (default: "en") |

By default, the service expects your Plex media library to be mounted at `/media`. If your files are located elsewhere, update `PLEX_LIBRARY_DIR` in `plex_subsync/config.py`.
 
## Docker

The PlexSubSync Docker image is available on GitHub Container Registry:

```bash
docker pull ghcr.io/ChrisHansenTech/PlexSubSync:latest
```

Or build the image locally:

```bash
docker build -t plexsubsync .
```

Run the container, mounting your Plex media library and setting environment variables:

```bash
docker run -d \
  --name plexsubsync \
  -p 8000:8000 \
  -v /path/to/media:/media \
  -e PLEX_TOKEN=<your_plex_token> \
  -e PLEX_URL=<your_plex_server_url> \
  -e DEFAULT_AUDIO_LANG=en \
  -e DEFAULT_SUB_LANG=en \
  -e HOME_ASSISTANT_WEBHOOK_URL=<optional_webhook_url> \
  ghcr.io/ChrisHansenTech/PlexSubSync:latest
```

Replace `/path/to/media` with the path to your Plex media library.

## API Usage

### Endpoint

```http
POST /subsync
Content-Type: application/json
```

### Payload

```json
{
  "media_id": 123456,                           # Plex metadata ID (integer)
  "entity_id": "media_player.living_room_tv",   # Home Assistant entity ID (optional)
  "audio_lang": "en",                           # ISO-639-1 audio language code (optional; default from DEFAULT_AUDIO_LANG env var, fallback: "en")
  "sub_lang": "es"                              # ISO-639-1 subtitle language code (optional; default from DEFAULT_SUB_LANG env var, fallback: "en")
}
```

The `media_id` corresponds to the Plex metadata ID of the media you want to sync. The optional `entity_id` is the Home Assistant entity ID and will be included in any notifications sent to your webhook. Audio and subtitle language codes are optional; if omitted, defaults are taken from the `DEFAULT_AUDIO_LANG` and `DEFAULT_SUB_LANG` environment variables (fallback: "en"). These codes help PlexSubSync match the correct audio track and subtitle file.

## Home Assistant Webhook Notification Payload

If `HOME_ASSISTANT_WEBHOOK_URL` is set, PlexSubSync will send HTTP POST requests to this URL with JSON payloads indicating the sync status:

```json
{
  "stage": "sync-started",
  "message": "SubSync started for: Movie Title",
  "media_id": 123456,
  "entity_id": "media_player.living_room_tv"
}
```

Fields:
- `stage`: One of `sync-started`, `sync-success`, or `sync-failed`.
- `message`: A human-readable message detailing the sync stage or error cause.
- `media_id`: The original Plex metadata ID from the request.
- `entity_id`: The Home Assistant entity ID provided in the request (if any).

Example success notification:

```json
{
  "stage": "sync-success",
  "message": "SubSync finished for: Movie Title",
  "media_id": 123456,
  "entity_id": "media_player.living_room_tv"
}
```

Example failure notification:

```json
{
  "stage": "sync-failed",
  "message": "SubSync failed for: Movie Title. Reason: No matching SRT file found",
  "media_id": 123456,
  "entity_id": "media_player.living_room_tv"
}
```

## Example Workflow

1. Use a Home Assistant script to send a REST command with the media ID and the entity playing the media.
2. Triggers a webhook to `PlexSubSync`.
3. `PlexSubSync` locates the media file and matches the appropriate subtitle file (e.g., based on language or filename) before calling `subsync` to synchronize timing.
4. Sends a status update to Home Assistant when the process is complete.
5. Home Assistant sends a push notification to your phone or restarts the media player to reload the updated subtitles.

This workflow is especially useful for syncing downloaded `.srt` files with variable timing quality. For more details, see [API Usage](#api-usage) and [Home Assistant Webhook Notification Payload](#home-assistant-webhook-notification-payload).

## Development

Run the service locally using Uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Logs will display information about the sync process, requests, and any errors encountered.

## Subtitle Matching

PlexSubSync looks for subtitle files in the same folder as the video file. It supports flexible extensions like:

- `.en.srt`
- `.eng.srt`
- `.en.sdh.srt`
- `.eng.sdh.srt`

It will pick the best match based on language and presence.

## License

This project is licensed under the MIT License.

Note: It depends on [`subsync`](https://github.com/sc0ty/subsync), which is licensed under GPL-3.0. Ensure your usage complies with the requirements of both licenses if redistributing or modifying.

---

### Created by [Chris Hansen](https://chrishansen.tech)

If you find this useful, feel free to star the repo, contribute, or reach out!
