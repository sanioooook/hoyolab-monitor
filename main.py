import asyncio, os, sys, datetime
from colorama import init
from config import LOCAL_TZ, DELAY, GENSHIN_UID, ZZZ_UID, HSR_UID
from version import VERSION
from utils.updater import check_for_updates
from client_factory import create_client
from data_fetcher import collect_data, collect_one_time_data, update_characters
from formatters.genshin_formatter import format_genshin
from formatters.zzz_formatter import format_ZZZ_notes, format_ZZZ_stats, format_ZZZ_temple, \
    format_shiyu_defense, format_deadly_assault
from formatters.hsr_formatter import (
    format_hsr_notes, format_hsr_anomaly_arbitration, format_hsr_apocalyptic_shadow,
    format_hsr_pure_fiction, format_hsr_challenge,
)
from utils.helpers import check_and_play_sound
from utils.progress import sleep_with_progress, animate_fetching
from utils.keyboard_listener import keyboard_listener

init()
check_for_updates(VERSION)


async def main_loop():
    client = await create_client()
    await update_characters()
    (genshin_spiral_abyss, genshin_theater, genshin_stygian_onslaught,
     hsr_anomaly_arb, hsr_apc_shadow, hsr_pure_fic, hsr_chall) = await collect_one_time_data(client)

    skip_event = asyncio.Event()
    last_fetch_time = [datetime.datetime.now(LOCAL_TZ)]
    asyncio.create_task(keyboard_listener(skip_event, last_fetch_time))

    try:
        while True:
            skip_event.clear()

            # Показываем анимацию пока идёт запрос данных
            spinner = asyncio.create_task(animate_fetching())
            genshin_note, zzz_note, zzz_stats, shiyu_defense, deadly_assault, hsr_note = await collect_data(client)
            last_fetch_time[0] = now = datetime.datetime.now(LOCAL_TZ)
            spinner.cancel()
            await asyncio.gather(spinner, return_exceptions=True)
            sys.stdout.write("\r" + " " * 50 + "\r")
            sys.stdout.flush()

            now = datetime.datetime.now(LOCAL_TZ)
            os.system("cls" if os.name == "nt" else "clear")

            genshin_section = format_genshin(genshin_note, genshin_spiral_abyss, genshin_theater, genshin_stygian_onslaught, now) if GENSHIN_UID else ""

            zzz_section = f"""ZZZ:
{format_ZZZ_notes(zzz_note, now)}
{format_shiyu_defense(shiyu_defense, now)}
{format_deadly_assault(deadly_assault, now)}{format_ZZZ_stats(zzz_stats, now)}
{format_ZZZ_temple(zzz_note, now)}""" if ZZZ_UID else ""

            hsr_section = f"""HSR:
{format_hsr_notes(hsr_note, now)}{format_hsr_anomaly_arbitration(hsr_anomaly_arb, now)}
{format_hsr_apocalyptic_shadow(hsr_apc_shadow, now)}
{format_hsr_pure_fiction(hsr_pure_fic, now)}
{format_hsr_challenge(hsr_chall, now)}""" if HSR_UID else ""

            sections = "\n\n".join(s for s in [genshin_section, zzz_section, hsr_section] if s)
            print(f"""{sections}
Event occurred on: {now.strftime('%d.%m.%Y %H:%M:%S')}""")

            if any([genshin_note, zzz_note, hsr_note]):
                check_and_play_sound(now, genshin_note, zzz_note, hsr_note)

            await sleep_with_progress(DELAY, skip_event)
    except KeyboardInterrupt:
        print("\n[Exit] Graceful shutdown.")


if __name__ == "__main__":
    asyncio.run(main_loop())
