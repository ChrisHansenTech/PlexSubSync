"""
Plex API client functions.
"""
import requests
from xml.etree import ElementTree as ET
from .config import PLEX_URL, PLEX_TOKEN

def get_plex_file_path(rating_key: str) -> str | None:
    """Retrieve the file path for a given Plex metadata rating_key."""
    try:
        url = f"{PLEX_URL}/library/metadata/{rating_key}?X-Plex-Token={PLEX_TOKEN}"
        response = requests.get(url)
        response.raise_for_status()

        root = ET.fromstring(response.text)
        part_element = root.find(".//Part")
        if part_element is not None:
            return part_element.attrib.get("file")
    except Exception as e:
        print(f"Error getting Plex metadata: {e}")
    return None
 
def get_plex_media_title(rating_key: str) -> str | None:
    """Retrieve the media title for a given Plex metadata rating_key."""
    try:
        url = f"{PLEX_URL}/library/metadata/{rating_key}?X-Plex-Token={PLEX_TOKEN}"
        response = requests.get(url)
        response.raise_for_status()
        root = ET.fromstring(response.text)
        # Look for Video element (movies, episodes) or Directory
        for tag in ("Video", "Directory"):
            elem = root.find(f".//{tag}")
            if elem is not None and "title" in elem.attrib:
                return elem.attrib.get("title")
    except Exception as e:
        print(f"Error getting Plex media title: {e}")
    return None