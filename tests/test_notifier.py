import requests
import pytest

import subsync_plex.notifier as notifier


class DummyResponse:
    def __init__(self, raise_exc=None):
        self._raise_exc = raise_exc

    def raise_for_status(self):
        if self._raise_exc:
            raise self._raise_exc


def test_send_notification_success(monkeypatch, capsys):
    monkeypatch.setattr(notifier, 'HOME_ASSISTANT_WEBHOOK_URL', 'http://example.com/webhook')
    monkeypatch.setattr(requests, 'post', lambda url, json: DummyResponse())
    notifier.send_home_assistant_notification('stage', 'message', 1, 'entity')
    captured = capsys.readouterr()
    assert 'Home Assistant webhook sent successfully.' in captured.out


def test_send_notification_failure(monkeypatch, capsys):
    monkeypatch.setattr(notifier, 'HOME_ASSISTANT_WEBHOOK_URL', 'http://example.com/webhook')
    def dummy_post(url, json):
        return DummyResponse(raise_exc=requests.RequestException('fail'))

    monkeypatch.setattr(requests, 'post', dummy_post)
    notifier.send_home_assistant_notification('stage', 'message', 2, 'entity2')
    captured = capsys.readouterr()
    assert 'Failed to send Home Assistant webhook' in captured.out