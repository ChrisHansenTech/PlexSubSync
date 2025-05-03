import os
import pytest

import subsync_plex.subtitle_finder as sf


@pytest.fixture(autouse=True)
def patch_plex_dir(tmp_path, monkeypatch):
    # Point library dir to temporary path
    monkeypatch.setattr(sf, 'PLEX_LIBRARY_DIR', str(tmp_path))
    return tmp_path


def create_files(tmp_path, directory, filenames):
    dir_path = tmp_path / directory
    dir_path.mkdir(parents=True, exist_ok=True)
    for name in filenames:
        (dir_path / name).write_text('')
    return dir_path


def test_no_directory():
    result = sf.find_matching_srt("nonexistent/video.mp4", "en")
    assert result is None


def test_iso1_match(tmp_path):
    dir_path = create_files(tmp_path, "movies", ["video.en.srt", "video.es.srt"])
    video_file = os.path.join("movies", "video.mp4")
    result = sf.find_matching_srt(video_file, "es")
    assert result == str(dir_path / "video.es.srt")


def test_iso2_fallback(tmp_path):
    dir_path = create_files(tmp_path, "movies", ["video.spa.srt"])
    video_file = os.path.join("movies", "video.mp4")
    result = sf.find_matching_srt(video_file, "es")
    assert result == str(dir_path / "video.spa.srt")


def test_forced_excluded(tmp_path):
    dir_path = create_files(tmp_path, "movies", ["video.en.forced.srt", "video.en.srt"])
    video_file = os.path.join("movies", "video.mp4")
    result = sf.find_matching_srt(video_file, "en")
    assert result == str(dir_path / "video.en.srt")


def test_no_language_code(tmp_path):
    dir_path = create_files(tmp_path, "movies", ["video.srt"])
    video_file = os.path.join("movies", "video.mp4")
    result = sf.find_matching_srt(video_file, "en")
    assert result is None