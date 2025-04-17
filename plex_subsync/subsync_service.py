"""
Core subtitle synchronization workflow.
"""
import subprocess
import os

from .plex_api import get_plex_file_path, get_plex_media_title
from .subtitle_finder import find_matching_srt
from .notifier import send_home_assistant_notification
from .config import (
    PLEX_LIBRARY_DIR,
    START_MESSAGE_TEMPLATE,
    NOTIFICATION_MESSAGE_TEMPLATE,
    FAILURE_MESSAGE_TEMPLATE,
)

def process_subsync(data) -> None:
    """
    Retrieve video file path from Plex, find matching subtitle, and run subsync.
    """
    video_file = get_plex_file_path(data.media_id)
    if not video_file:
        print("Error: Unable to fetch file path from Plex.")
        return
    video_file = video_file.lstrip("/")
    # Retrieve media title for notifications
    title = get_plex_media_title(data.media_id)
    if not title:
        title = os.path.splitext(os.path.basename(video_file))[0]
    srt_file = find_matching_srt(video_file, data.sub_lang)
    if not srt_file:
        print("Error: No matching SRT file found.")
        return

    ref_file = os.path.join(PLEX_LIBRARY_DIR, video_file)
    print(f"Reference video: {ref_file}")
    print(f"Subtitle file: {srt_file}")
    send_home_assistant_notification(START_MESSAGE_TEMPLATE.format(title))

    try:
        result = subprocess.run(
            [
                "subsync",
                "--cli",
                "sync",
                "--ref", ref_file,
                "--ref-lang", data.audio_lang,
                "--sub", srt_file,
                "--sub-lang", data.sub_lang,
                "--out", srt_file,
                "--overwrite",
                "--effort", "1"
            ],
            check=True,
            capture_output=False,
            text=True
        )
        print(f"SubSync output: {result.stdout}")
        send_home_assistant_notification(NOTIFICATION_MESSAGE_TEMPLATE.format(title))
    except subprocess.CalledProcessError as e:
        print(f"SubSync error: {e.stderr}")
        send_home_assistant_notification(FAILURE_MESSAGE_TEMPLATE.format(title))