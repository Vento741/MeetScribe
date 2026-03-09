from src.storage.database import Meeting
from src.storage.exporter import export_to_markdown

def test_export_creates_md_file(tmp_path):
    meeting = Meeting(
        id=1, title="Тест", date="2026-03-09T10:00:00",
        duration=3600, audio_path="", transcript="Транскрипт тут",
        summary="# Протокол\n## Решения\n1. Тест", prompt_used="",
        created_at="2026-03-09",
    )
    path = export_to_markdown(meeting, tmp_path)
    assert path.exists()
    assert path.suffix == ".md"
    content = path.read_text(encoding="utf-8")
    assert "Тест" in content
    assert "Протокол" in content

def test_export_filename_format(tmp_path):
    meeting = Meeting(
        id=1, title="Планёрка", date="2026-03-09T14:30:00",
        duration=1800, audio_path="", transcript="", summary="Саммари",
        prompt_used="", created_at="2026-03-09",
    )
    path = export_to_markdown(meeting, tmp_path)
    assert "2026-03-09" in path.name
    assert "Планёрка" in path.name
