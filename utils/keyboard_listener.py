import asyncio
import time


async def keyboard_listener(skip_event: asyncio.Event, cooldown: int = 60) -> None:
    """
    Listens for R/r key press and sets skip_event to trigger an early refresh.
    Enforces a cooldown between manual triggers to avoid API rate limits.
    Windows-only (msvcrt). No-op on other platforms.
    """
    try:
        import msvcrt
    except ImportError:
        return

    last_triggered = 0.0

    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key in (b'r', b'R'):
                now = time.monotonic()
                if now - last_triggered >= cooldown:
                    skip_event.set()
                    last_triggered = now
        await asyncio.sleep(0.1)
