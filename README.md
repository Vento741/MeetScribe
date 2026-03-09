<p align="center">
  <img src="https://raw.githubusercontent.com/Vento741/MeetScribe/main/src/assets/icon.ico" width="120" alt="MeetScribe icon"/>
</p>

<h1 align="center">MeetScribe</h1>

<p align="center">
  <b>Автоматический протокол видеоконференций</b><br/>
  <sub>Запись системного звука + микрофона · Транскрибация через Gemini · AI-саммари с решениями и action items</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11+-3776ab?logo=python&logoColor=white" alt="Python 3.11+"/>
  <img src="https://img.shields.io/badge/platform-Windows-0078D6?logo=windows&logoColor=white" alt="Windows"/>
  <img src="https://img.shields.io/badge/GUI-CustomTkinter-2BA5B5" alt="CustomTkinter"/>
  <img src="https://img.shields.io/badge/AI-Gemini%20via%20OpenRouter-FF6F00?logo=google&logoColor=white" alt="Gemini"/>
  <img src="https://img.shields.io/badge/version-1.0.1-green" alt="Version"/>
</p>

---

## Что это?

**MeetScribe** — десктопное приложение для Windows, которое записывает звук видеоконференций (Яндекс.Телемост, Zoom, Google Meet и др.), автоматически транскрибирует речь и генерирует структурированный протокол встречи с помощью AI.

Никаких плагинов к браузеру, никаких ботов в конференции — MeetScribe работает тихо на уровне системного аудио через WASAPI loopback.

### Ключевые возможности

| Возможность | Описание |
|---|---|
| **Двухканальная запись** | Системный звук (WASAPI loopback) + микрофон одновременно с автоматической синхронизацией дорожек |
| **AI-транскрибация** | Распознавание речи с определением спикеров через Gemini (OpenRouter API) |
| **Умное саммари** | Структурированный протокол: резюме, решения, action items, ответственные, сроки |
| **Полнотекстовый поиск** | SQLite FTS5 — мгновенный поиск по всем транскриптам и саммари |
| **Экспорт** | PDF, Markdown, HTML, TXT — с поддержкой кириллицы |
| **Папки и организация** | Drag & drop встреч между папками, контекстное меню |
| **Перегенерация саммари** | Повторная генерация с другим промптом без повторной транскрибации |
| **Горячие клавиши** | Глобальный хоткей `Ctrl+Shift+R` для старта/стопа записи из любого приложения |
| **Тёмная/светлая тема** | Переключение в настройках |

---

## Скриншоты

<details>
<summary><b>Экран записи</b></summary>

Таймер, индикаторы уровня микрофона и системного звука в реальном времени.

</details>

<details>
<summary><b>История встреч</b></summary>

Компактные карточки с датой, названием и длительностью. Папки, поиск, drag & drop.

</details>

<details>
<summary><b>Просмотр протокола</b></summary>

Вкладки «Саммари» и «Транскрипт». Кнопки экспорта, перегенерации, копирования.

</details>

---

## Быстрый старт

### Требования

- **Windows 10/11** (WASAPI loopback — только Windows)
- **Python 3.11+**
- **API ключ OpenRouter** — [получить здесь](https://openrouter.ai/keys)

### Установка из исходников

```bash
# 1. Клонируем репозиторий
git clone https://github.com/Vento741/MeetScribe.git
cd MeetScribe

# 2. Создаём виртуальное окружение
python -m venv venv
venv\Scripts\activate

# 3. Устанавливаем зависимости
pip install -r requirements.txt

# 4. Запускаем
python src/main.py
```

### Сборка .exe

См. раздел [Сборка .exe](#сборка-exe) ниже.

---

## Настройка

При первом запуске откройте **Настройки** (⚙ в боковой панели):

| Параметр | Описание |
|---|---|
| **API ключ OpenRouter** | Ваш ключ для доступа к Gemini. Хранится локально в `%APPDATA%/MeetScribe/config.json` |
| **Модель** | По умолчанию `google/gemini-3.1-flash-lite-preview` — быстрая и экономичная. Можно сменить на любую модель OpenRouter |
| **Микрофон** | Выберите ваш микрофон (только WASAPI-устройства) |
| **Системный звук** | Выберите loopback-устройство (обычно — ваши динамики/наушники) |
| **Горячая клавиша** | Комбинация для старта/стопа записи. По умолчанию `Ctrl+Shift+R` |
| **Папка сохранения** | Куда сохранять экспортированные файлы. По умолчанию `Документы/MeetScribe` |
| **Шаблон промпта** | Настраиваемый промпт для генерации саммари — определяет структуру протокола |

---

## Как это работает

```
┌─────────────┐     ┌─────────────┐
│  Микрофон    │     │  Системный  │
│  (WASAPI)    │     │  звук       │
│  sounddevice │     │  loopback   │
└──────┬───────┘     └──────┬──────┘
       │                    │
       │  синхронизация     │  gap-filling
       │  по таймстемпам    │  (тишина для пауз)
       └────────┬───────────┘
                │
         ┌──────▼──────┐
         │   Микшер    │
         │  (16 kHz    │
         │   моно)     │
         └──────┬──────┘
                │
    ┌───────────▼───────────┐
    │   Чанкинг (10 мин)   │
    │   + перекрытие 30с    │
    └───────────┬───────────┘
                │
    ┌───────────▼───────────┐
    │   Gemini API          │
    │   (параллельная       │
    │    транскрибация)     │
    └───────────┬───────────┘
                │
    ┌───────────▼───────────┐
    │   Генерация саммари   │
    │   (настраиваемый      │
    │    промпт)            │
    └───────────┬───────────┘
                │
    ┌───────────▼───────────┐
    │   SQLite + FTS5       │
    │   (сохранение и       │
    │    полнотекстовый     │
    │    поиск)             │
    └───────────────────────┘
```

### Синхронизация аудио

Главная техническая сложность — WASAPI loopback **не генерирует сэмплы**, когда нет системного звука. MeetScribe решает это двумя механизмами:

1. **Начальное смещение** — время первого сэмпла каждой дорожки фиксируется, и более поздняя дорожка дополняется тишиной в начале
2. **Gap-filling** — промежутки тишины внутри loopback-потока детектируются по таймстемпам колбэков и заполняются тишиной соответствующей длительности

Результат: дорожки микрофона и системного звука идеально совпадают по времени.

---

## Структура проекта

```
src/
├── main.py                  # Точка входа
├── app.py                   # Главное окно, навигация, горячие клавиши
├── config.py                # Конфигурация (dataclass + JSON)
├── audio/
│   ├── recorder.py          # Двухканальная запись: WASAPI loopback + микрофон
│   └── mixer.py             # Микширование и ресемплирование дорожек
├── ai/
│   ├── openrouter_client.py # HTTP-клиент OpenRouter API (httpx async)
│   ├── transcriber.py       # Чанкинг аудио + параллельная транскрибация
│   └── summarizer.py        # Генерация структурированного саммари
├── storage/
│   ├── database.py          # SQLite: meetings, folders, FTS5, миграции
│   └── exporter.py          # Экспорт в PDF/MD/HTML/TXT
├── ui/
│   ├── sidebar.py           # Боковая панель навигации
│   ├── recording_view.py    # Экран записи: таймер, VU-метры
│   ├── history_view.py      # История: карточки, папки, drag & drop, поиск
│   ├── transcript_view.py   # Просмотр: вкладки саммари/транскрипт, экспорт
│   ├── settings_view.py     # Настройки: устройства, API, промпт
│   └── hotkeys.py           # Глобальные горячие клавиши (pynput Listener)
└── assets/
    └── icon.ico             # Иконка приложения
```

---

## Сборка .exe

```bash
# Активируем venv
venv\Scripts\activate

# Устанавливаем PyInstaller (если ещё нет)
pip install pyinstaller

# Собираем
pyinstaller --onefile --windowed \
  --icon=src/assets/icon.ico \
  --name=MeetScribe \
  --add-data "src/assets/icon.ico;assets" \
  --paths=src \
  src/main.py
```

Готовый `MeetScribe.exe` появится в папке `dist/`.

---

## Разработка

```bash
# Запуск
python src/main.py

# Тесты
pytest tests/ -v

# Линтер
ruff check src/

# Форматирование
ruff format src/

# Проверка типов
mypy src/ --ignore-missing-imports
```

### Переменные окружения

| Переменная | Описание |
|---|---|
| `OPENROUTER_API_KEY` | Переопределяет API ключ из конфига |
| `MEETSCRIBE_DEBUG` | Установите `1` для подробного логирования |

---

## Зависимости

| Пакет | Назначение |
|---|---|
| `customtkinter` | GUI-фреймворк (тёмная/светлая тема) |
| `sounddevice` | Запись с микрофона (WASAPI) |
| `pyaudiowpatch` | WASAPI loopback (системный звук) |
| `soundfile` | Чтение/запись WAV |
| `httpx` | Асинхронные HTTP-запросы к OpenRouter API |
| `pynput` | Глобальные горячие клавиши |
| `Pillow` | Работа с изображениями |
| `fpdf2` | Генерация PDF с кириллицей |
| `markdown` | Конвертация Markdown → HTML для экспорта |

---

## Хранение данных

| Что | Где |
|---|---|
| Конфигурация | `%APPDATA%/MeetScribe/config.json` |
| База данных | `%APPDATA%/MeetScribe/meetings.db` |
| Временные аудиофайлы | `%TEMP%/MeetScribe/` |
| Экспортированные файлы | `Документы/MeetScribe/` (настраивается) |

---

## Лицензия

MIT

---

<p align="center">
  <sub>Разработано <a href="https://github.com/Vento741">Web Dusha</a></sub>
</p>
