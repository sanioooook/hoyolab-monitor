import asyncio
import datetime
from config import LOCAL_TZ


async def keyboard_listener(
    skip_event: asyncio.Event,
    last_fetch_time: list[datetime.datetime],
    cooldown: int = 60,
) -> None:
    """
    Listens for R/r key press and sets skip_event to trigger an early refresh.
    Cooldown is measured from the last completed fetch, not the last key press.
    Windows-only (msvcrt). No-op on other platforms.
    """
    try:
        import msvcrt
    except ImportError:
        return

    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key in (b'r', b'R'):
                elapsed = (datetime.datetime.now(LOCAL_TZ) - last_fetch_time[0]).total_seconds()
                if elapsed >= cooldown:
                    skip_event.set()
        await asyncio.sleep(0.1)
