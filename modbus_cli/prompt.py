"""Utilities for prompting user input."""

from __future__ import annotations

from typing import Callable, Optional


class PromptService:
    """Centralized helper for user prompts, casting, and defaults."""

    def __init__(self, input_func: Callable[[str], str] = input) -> None:
        self._input = input_func

    def prompt(
        self,
        message: str,
        default: Optional[str] = None,
        cast: Callable[[str], object] = str,
    ):
        suffix = f" [{default}]" if default is not None else ""
        raw = self._input(f"{message}{suffix}: ").strip()
        if not raw:
            if default is None:
                raise ValueError("Input tidak boleh kosong")
            raw = str(default)
        try:
            return cast(raw)
        except Exception as exc:  # pragma: no cover - interactive helper
            print(f"⚠️  Nilai tidak valid ({exc}). Coba lagi.")
            return self.prompt(message, default, cast)
