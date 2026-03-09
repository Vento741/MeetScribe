import sys
from pathlib import Path

# Добавляем src/ в sys.path, чтобы внутренние импорты работали в тестах
sys.path.insert(0, str(Path(__file__).parent / "src"))
