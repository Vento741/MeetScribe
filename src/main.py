import logging
import os
import sys
from pathlib import Path

# Добавляем src в путь для импортов при запуске как .exe
sys.path.insert(0, str(Path(__file__).parent))

from app import MeetScribeApp


def main() -> None:
    """Точка входа в приложение."""
    logging.basicConfig(
        level=logging.DEBUG if os.environ.get("MEETSCRIBE_DEBUG") else logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )
    app = MeetScribeApp()
    app.mainloop()


if __name__ == "__main__":
    main()
