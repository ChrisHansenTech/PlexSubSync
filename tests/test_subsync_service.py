import subprocess

import subsync_plex.subsync_service as service


class DummyData:
    def __init__(self, media_id, entity_id=None, audio_lang=None, sub_lang=None):
        self.media_id = media_id
        self.entity_id = entity_id
        self.audio_lang = audio_lang
        self.sub_lang = sub_lang


def test_process_subsync_no_srt(monkeypatch, capsys):
    # Setup: no matching subtitle
    monkeypatch.setattr(service, 'get_plex_file_path', lambda media_id: "movies/video.mp4")
    monkeypatch.setattr(service, 'get_plex_media_title', lambda media_id: "Test Video")
    monkeypatch.setattr(service, 'find_matching_srt', lambda video_file, lang: None)
    calls = []

    def fake_notify(stage, message, media_id, entity_id):
        calls.append((stage, message, media_id, entity_id))

    monkeypatch.setattr(service, 'send_home_assistant_notification', fake_notify)
    data = DummyData(media_id=42, entity_id='ent1')
    service.process_subsync(data)
    # Only failure notification should be sent
    assert len(calls) == 1
    stage, message, media_id, entity_id = calls[0]
    assert stage == service.STAGE_SYNC_FAILED
    assert "No matching SRT file found" in message
    assert media_id == 42
    assert entity_id == 'ent1'


def test_process_subsync_success(monkeypatch):
    monkeypatch.setattr(service, 'get_plex_file_path', lambda media_id: "movies/video.mp4")
    monkeypatch.setattr(service, 'get_plex_media_title', lambda media_id: "Test Video")
    # Provide a fake subtitle path
    srt_path = "/media/movies/video.en.srt"
    monkeypatch.setattr(service, 'find_matching_srt', lambda video_file, lang: srt_path)
    calls = []

    def fake_notify(stage, message, media_id, entity_id):
        calls.append((stage, message, media_id, entity_id))

    monkeypatch.setattr(service, 'send_home_assistant_notification', fake_notify)
    # Dummy subprocess run
    class DummyCompleted:
        def __init__(self):
            self.stdout = "ok"

    monkeypatch.setattr(subprocess, 'run', lambda *args, **kwargs: DummyCompleted())
    data = DummyData(media_id=43, entity_id='ent2', audio_lang='en', sub_lang='en')
    service.process_subsync(data)
    # Two notifications: start and finish
    assert len(calls) == 2
    assert calls[0][0] == service.STAGE_SYNC_START
    assert calls[1][0] == service.STAGE_SYNC_FINISHED
    # Check media_id and entity_id propagation
    assert calls[0][2] == 43 and calls[0][3] == 'ent2'
    assert calls[1][2] == 43 and calls[1][3] == 'ent2'