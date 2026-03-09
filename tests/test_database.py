from datetime import datetime
from src.storage.database import MeetingDB, Meeting

def test_create_and_get_meeting(tmp_path):
    db = MeetingDB(tmp_path / "test.db")
    meeting_id = db.create_meeting(
        title="Планёрка",
        date=datetime.now().isoformat(),
        duration=3600,
        audio_path="/tmp/test.wav",
        transcript="Обсуждали запуск",
        summary="# Протокол\n## Решения\n1. Запуск в апреле",
        prompt_used="default",
    )
    assert meeting_id == 1
    meeting = db.get_meeting(meeting_id)
    assert meeting.title == "Планёрка"
    assert meeting.duration == 3600
    db.close()

def test_list_meetings(tmp_path):
    db = MeetingDB(tmp_path / "test.db")
    db.create_meeting("Встреча 1", "2026-03-01", 1800, "", "", "", "")
    db.create_meeting("Встреча 2", "2026-03-02", 2400, "", "", "", "")
    meetings = db.list_meetings()
    assert len(meetings) == 2
    assert meetings[0].title == "Встреча 2"  # newest first
    db.close()

def test_search_meetings(tmp_path):
    db = MeetingDB(tmp_path / "test.db")
    db.create_meeting("Ретро", "2026-03-01", 1800, "", "спринт дизайн ревью", "", "")
    db.create_meeting("Планёрка", "2026-03-02", 1200, "", "бюджет финансы", "", "")
    results = db.search("дизайн")
    assert len(results) == 1
    assert results[0].title == "Ретро"
    db.close()

def test_update_meeting_title(tmp_path):
    db = MeetingDB(tmp_path / "test.db")
    mid = db.create_meeting("Без названия", "2026-03-01", 600, "", "", "", "")
    db.update_title(mid, "Стендап")
    meeting = db.get_meeting(mid)
    assert meeting.title == "Стендап"
    db.close()

def test_delete_meeting(tmp_path):
    db = MeetingDB(tmp_path / "test.db")
    mid = db.create_meeting("Удалить", "2026-03-01", 600, "", "", "", "")
    db.delete_meeting(mid)
    assert db.get_meeting(mid) is None
    db.close()
