from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
from subsync_plex.subsync_service import process_subsync

app = FastAPI()

class PlexRequest(BaseModel):
    media_id: int
    entity_id: Optional[str] = None
    # ISO-639-1 audio language code; optional, defaults to environment or 'en'
    audio_lang: Optional[str] = None
    # ISO-639-1 subtitle language code; optional, defaults to environment or 'en'
    sub_lang: Optional[str] = None

@app.post("/subsync")
async def run_subsync(data: PlexRequest, background_tasks: BackgroundTasks):
    """Schedule a subtitle sync in the background."""
    background_tasks.add_task(process_subsync, data)
    return ""