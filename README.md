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

> Looking for a containerized version? Check out [PlexSubSync-Docker](https://github.com/ChrisHansenTech/PlexSubSync-Docker)

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

By default, the service expects your Plex media library to be mounted at `/media`. If your files are located elsewhere, update `PLEX_LIBRARY_DIR` in `plex_subsync/config.py`.

## API Usage

### Endpoint

```http
POST /subsync
Content-Type: application/json
```

### Payload

```json
{
  "media_id": "123456",      # Plex metadata ID
  "audio_lang": "en",        # ISO-639-1 audio language code
  "sub_lang": "es"           # ISO-639-1 subtitle language code
}
```

The `media_id` corresponds to the Plex metadata ID of the media you want to sync. Provide both audio and subtitle language codes so that PlexSubSync can match the correct audio track and subtitle file.

## Example Workflow

1. Home Assistant detects playback ending
2. Triggers a webhook to `PlexSubSync`
3. `PlexSubSync` looks up the file, finds the subtitle, and calls `subsync`
4. Notifies Home Assistant when finished

This is especially useful for syncing downloaded `.srt` files with variable timing quality.

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
