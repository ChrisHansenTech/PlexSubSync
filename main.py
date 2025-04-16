from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import subprocess
import requests
import os
import glob

app = FastAPI()

# CONFIGURE THESE
PLEX_URL = os.getenv("PLEX_URL")
PLEX_TOKEN = os.getenv("PLEX_TOKEN")
HOME_ASSISTANT_WEBHOOK_URL = os.getenv("HOME_ASSISTANT_WEBHOOK_URL")

NOTIFICATION_MESSAGE_TEMPLATE = "SubSync finished for: {}"
START_MESSAGE_TEMPLATE = "SubSync started for: {}"
FAILURE_MESSAGE_TEMPLATE = "SubSync failed for: {}"

PLEX_LIBRARY_DIR = "/media"

class PlexRequest(BaseModel):
    media_content_id: str  # This should be the Plex ratingKey

@app.post("/subsync")
async def run_subsync(data: PlexRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_subsync, data.media_content_id)
    return ""

def process_subsync(rating_key: str):
    video_file = get_plex_file_path(rating_key)
    video_file = video_file.lstrip("/")
    if not video_file:
        print("Error: Unable to fetch file path from Plex.")
        return

    srt_file = find_matching_srt(video_file)
    if not srt_file:
        print("Error: No matching SRT file found.")
        return

    ref_file = os.path.join(PLEX_LIBRARY_DIR, video_file)
    print(f"Reference video: {ref_file}")
    print(f"Subtitle file: {srt_file}")

    send_home_assistant_notification(START_MESSAGE_TEMPLATE.format(video_file))

    try:
        result = subprocess.run(
            [
                "subsync",
                "--cli",
                "sync",
                "--ref", ref_file,
                "--ref-lang", "en",
                "--sub", srt_file,
                "--sub-lang", "en",
                "--out", srt_file,
                "--overwrite",
                "--effort", "1"
            ],
            check=True,
            capture_output=False,
            text=True
        )
        print(f"SubSync output: {result.stdout}")
        send_home_assistant_notification(NOTIFICATION_MESSAGE_TEMPLATE.format(video_file))
    except subprocess.CalledProcessError as e:
        print(f"SubSync error: {e.stderr}")
        send_home_assistant_notification(FAILURE_MESSAGE_TEMPLATE.format(video_file))

def send_home_assistant_notification(message):
    try:
        response = requests.post(HOME_ASSISTANT_WEBHOOK_URL, json={"message": message})
        response.raise_for_status()
        print("Home Assistant webhook sent successfully.")
    except requests.RequestException as e:
        print(f"Failed to send Home Assistant webhook: {e}")


def get_plex_file_path(rating_key: str) -> str:
    try:
        url = f"{PLEX_URL}/library/metadata/{rating_key}?X-Plex-Token={PLEX_TOKEN}"
        response = requests.get(url)
        response.raise_for_status()

        # Basic XML parsing (you could use xml.etree if desired)
        from xml.etree import ElementTree as ET
        root = ET.fromstring(response.text)

        # Extract file path from <Part file="..."/>
        part_element = root.find(".//Part")
        if part_element is not None:
            return part_element.attrib.get("file")

    except Exception as e:
        print(f"Error getting Plex metadata: {e}")
    return None

def find_matching_srt(video_file: str) -> str | None:
    base_name = os.path.splitext(video_file)[0]
    video_dir = os.path.join(PLEX_LIBRARY_DIR, os.path.dirname(video_file))
    
    print(video_dir)
    candidates = glob.glob(os.path.join(video_dir, os.path.basename(base_name) + "*.srt"))

    return candidates[0] if candidates else None

