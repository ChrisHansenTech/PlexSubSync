"""
Core subtitle synchronization workflow.
"""
import subprocess
import os

from .plex_api import get_plex_file_path, get_plex_media_title
from .subtitle_finder import find_matching_srt
from .notifier import send_home_assistant_notification
from .config import *

def process_subsync(data) -> None:
    """
    Retrieve video file path from Plex, find matching subtitle, and run subsync.
    """
    # determine language codes (request overrides environment variable, fallback to 'en')
    audio_lang = data.audio_lang or DEFAULT_AUDIO_LANG
    sub_lang = data.sub_lang or DEFAULT_SUB_LANG
    video_file = get_plex_file_path(data.media_id)
    if not video_file:
        print("Error: Unable to fetch file path from Plex.", flush=True)
        return
    video_file = video_file.lstrip("/")
    # Retrieve media title for notifications
    title = get_plex_media_title(data.media_id)
    if not title:
        title = os.path.splitext(os.path.basename(video_file))[0]
    srt_file = find_matching_srt(video_file, sub_lang)
    if not srt_file:
        # notify failure with reason when subtitle is missing
        reason = "No matching SRT file found"
        print(f"Error: {reason}.", flush=True)
        send_home_assistant_notification(
            STAGE_SYNC_FAILED,
            FAILURE_MESSAGE_TEMPLATE.format(title, reason),
            data.media_id,
            data.entity_id,
        )
        return

    ref_file = os.path.join(PLEX_LIBRARY_DIR, video_file)
    print(f"Reference video: {ref_file}", flush=True)
    print(f"Subtitle file: {srt_file}", flush=True)
    send_home_assistant_notification(
        STAGE_SYNC_START,
        START_MESSAGE_TEMPLATE.format(title),
        data.media_id,
        data.entity_id
    )

    try:
        result = subprocess.run(
            [
                "subsync",
                "--cli",
                "sync",
                "--ref", ref_file,
                "--ref-lang", audio_lang,
                "--sub", srt_file,
                "--sub-lang", sub_lang,
                "--out", srt_file,
                "--overwrite",
                "--effort", "1"
            ],
            check=True,
            capture_output=False,
            text=True
        )
        print(f"SubSync output: {result.stdout}", flush=True)
        send_home_assistant_notification(
            STAGE_SYNC_FINISHED,
            NOTIFICATION_MESSAGE_TEMPLATE.format(title),
            data.media_id,
            data.entity_id
        )
    except subprocess.CalledProcessError as e:
        # include subprocess error details in notification
        reason = e.stderr or str(e)
        print(f"SubSync error: {reason}", flush=True)
        send_home_assistant_notification(
            STAGE_SYNC_FAILED,
            FAILURE_MESSAGE_TEMPLATE.format(title, reason),
            data.media_id,
            data.entity_id
        )