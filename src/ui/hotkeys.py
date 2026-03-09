from __future__ import annotations

import logging
from typing import Callable

from pynput import keyboard

logger = logging.getLogger(__name__)


class GlobalHotkeys:
    """Глобальные горячие клавиши для управления записью.

    Использует keyboard.Listener с ручным отслеживанием нажатых клавиш,
    что надёжнее GlobalHotKeys на Windows.
    """

    _MODIFIER_MAP = {
        "ctrl": {keyboard.Key.ctrl_l, keyboard.Key.ctrl_r},
        "control": {keyboard.Key.ctrl_l, keyboard.Key.ctrl_r},
        "shift": {keyboard.Key.shift_l, keyboard.Key.shift_r},
        "alt": {keyboard.Key.alt_l, keyboard.Key.alt_r, keyboard.Key.alt_gr},
    }

    def __init__(self) -> None:
        self._listener: keyboard.Listener | None = None
        self._bindings: list[tuple[set, str, Callable]] = []
        self._pressed_keys: set = set()

    def register(self, hotkey: str, callback: Callable) -> None:
        """Регистрирует горячую клавишу с указанным колбэком.

        Формат: 'ctrl+shift+r', 'alt+f1' и т.д.
        """
        parts = hotkey.lower().replace(" ", "").split("+")
        modifiers: set = set()
        key_char: str = ""

        for p in parts:
            if p in self._MODIFIER_MAP:
                modifiers.update(self._MODIFIER_MAP[p])
            else:
                key_char = p

        self._bindings.append((modifiers, key_char, callback))
        logger.debug("Зарегистрирована горячая клавиша: %s", hotkey)

    def start(self) -> None:
        """Запускает прослушивание горячих клавиш."""
        if self._listener:
            self.stop()
        if not self._bindings:
            return
        try:
            self._listener = keyboard.Listener(
                on_press=self._on_press,
                on_release=self._on_release,
            )
            self._listener.daemon = True
            self._listener.start()
            logger.info(
                "Горячие клавиши активны (%d привязок)", len(self._bindings)
            )
        except Exception as e:
            logger.error("Не удалось запустить прослушивание клавиш: %s", e)

    def stop(self) -> None:
        """Останавливает прослушивание горячих клавиш."""
        if self._listener:
            self._listener.stop()
            self._listener = None
            self._pressed_keys.clear()

    def _on_press(self, key: keyboard.Key | keyboard.KeyCode | None) -> None:
        """Обработчик нажатия клавиши."""
        if key is None:
            return
        self._pressed_keys.add(key)
        self._check_bindings(key)

    def _on_release(self, key: keyboard.Key | keyboard.KeyCode | None) -> None:
        """Обработчик отпускания клавиши."""
        self._pressed_keys.discard(key)

    def _check_bindings(self, key: keyboard.Key | keyboard.KeyCode) -> None:
        """Проверяет, совпадает ли текущая комбинация с зарегистрированными."""
        for modifiers, key_char, callback in self._bindings:
            # Проверяем, что все нужные модификаторы нажаты
            mods_ok = all(
                any(m in self._pressed_keys for m in self._MODIFIER_MAP[name])
                for name in ("ctrl", "shift", "alt")
                if self._MODIFIER_MAP.get(name, set()) & modifiers
            )
            if not mods_ok:
                continue

            # Проверяем основную клавишу
            char_ok = False
            if isinstance(key, keyboard.KeyCode):
                if key.char and key.char.lower() == key_char:
                    char_ok = True
                elif key.vk is not None:
                    # Fallback: проверка по виртуальному коду
                    # (когда char=None из-за зажатого Ctrl)
                    expected_vk = ord(key_char.upper()) if len(key_char) == 1 else None
                    if expected_vk and key.vk == expected_vk:
                        char_ok = True
            elif isinstance(key, keyboard.Key):
                if key.name == key_char:
                    char_ok = True

            if char_ok:
                try:
                    callback()
                except Exception as e:
                    logger.error("Ошибка в обработчике горячей клавиши: %s", e)
