import requests
import pytest

import subsync_plex.plex_api as plex_api


class DummyResponse:
    def __init__(self, text='', raise_exc=None):
        self.text = text
        self._raise_exc = raise_exc

    def raise_for_status(self):
        if self._raise_exc:
            raise self._raise_exc


def test_get_plex_file_path_success(monkeypatch):
    xml = '<MediaContainer><Video><Part file="/media/movie.mp4"/></Video></MediaContainer>'
    dummy = DummyResponse(text=xml)
    monkeypatch.setattr(requests, 'get', lambda url: dummy)
    path = plex_api.get_plex_file_path(123)
    assert path == "/media/movie.mp4"


def test_get_plex_file_path_failure(monkeypatch, capsys):
    err = requests.RequestException("bad request")
    dummy = DummyResponse(text='', raise_exc=err)
    monkeypatch.setattr(requests, 'get', lambda url: dummy)
    path = plex_api.get_plex_file_path(456)
    assert path is None
    captured = capsys.readouterr()
    assert "Error getting Plex metadata" in captured.out


def test_get_plex_media_title_video(monkeypatch):
    xml = '<MediaContainer><Video title="Test Movie"/></MediaContainer>'
    dummy = DummyResponse(text=xml)
    monkeypatch.setattr(requests, 'get', lambda url: dummy)
    title = plex_api.get_plex_media_title(123)
    assert title == "Test Movie"


def test_get_plex_media_title_directory(monkeypatch):
    xml = '<MediaContainer><Directory title="Test Folder"/></MediaContainer>'
    dummy = DummyResponse(text=xml)
    monkeypatch.setattr(requests, 'get', lambda url: dummy)
    title = plex_api.get_plex_media_title(789)
    assert title == "Test Folder"


def test_get_plex_media_title_none(monkeypatch, capsys):
    monkeypatch.setattr(requests, 'get', lambda url: DummyResponse(text='<bad>'))
    title = plex_api.get_plex_media_title(0)
    assert title is None
    captured = capsys.readouterr()
    assert "Error getting Plex media title" in captured.out