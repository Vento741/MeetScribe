from __future__ import annotations

from ai.openrouter_client import send_chat_request


async def generate_summary(
    transcript: str,
    prompt_template: str,
    api_key: str,
    model: str = "google/gemini-3.1-flash-lite-preview",
) -> str:
    """Генерирует структурированное саммари встречи по транскрипту."""
    messages = [
        {"role": "system", "content": prompt_template},
        {"role": "user", "content": f"Вот транскрипт встречи:\n\n{transcript}"},
    ]

    return await send_chat_request(messages, api_key, model)
