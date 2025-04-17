from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from plex_subsync.subsync_service import process_subsync

app = FastAPI()

class PlexRequest(BaseModel):
    media_id: str
    audio_lang: str
    sub_lang: str

@app.post("/subsync")
async def run_subsync(data: PlexRequest, background_tasks: BackgroundTasks):
    """Schedule a subtitle sync in the background."""
    background_tasks.add_task(process_subsync, data)
    return ""