import asyncio
import sys
from typing import Optional


async def animate_fetching() -> None:
    """
    Показывает анимацию спиннера пока идёт запрос данных.
    Запускать как asyncio.create_task(), отменять после завершения fetch.
    """
    frames = ["|", "/", "-", "\\"]
    i = 0
    while True:
        sys.stdout.write(f"\rЗапрос данных... {frames[i % len(frames)]}")
        sys.stdout.flush()
        i += 1
        await asyncio.sleep(0.1)


async def sleep_with_progress(
    total_seconds: int,
    skip_event: Optional[asyncio.Event] = None,
) -> None:
    """
    Заменяет asyncio.sleep(DELAY). Выводит прогресс-бар обратного отсчёта внизу экрана.
    Обновляется раз в секунду через \\r — минимальная нагрузка на систему.

    Args:
        total_seconds: Общее время ожидания в секундах.
        skip_event:    asyncio.Event для досрочного выхода (фаза 2 — ручной запуск).
    """
    BAR_WIDTH = 32

    for elapsed in range(total_seconds):
        if skip_event and skip_event.is_set():
            break

        remaining = total_seconds - elapsed
        filled = round(BAR_WIDTH * elapsed / total_seconds)
        bar = "█" * filled + "░" * (BAR_WIDTH - filled)
        mins, secs = divmod(remaining, 60)
        line = f"\rСледующее обновление: [{bar}] {mins:02}:{secs:02}"
        sys.stdout.write(line)
        sys.stdout.flush()
        await asyncio.sleep(1)

    # Очистить строку перед следующей итерацией
    sys.stdout.write("\r" + " " * 60 + "\r")
    sys.stdout.flush()
