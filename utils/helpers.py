import datetime
from genshin.models import Notes, ZZZNotes
from config import LOCAL_TZ
from utils.sound import play_sound


def check_and_play_sound(genshin_note: Notes, zzz_note: ZZZNotes, now: datetime.datetime):
    now_plus_one_day = now + datetime.timedelta(days=1)
    datetime_reset_hoyo_servers = datetime.datetime(day=now_plus_one_day.day, month=now_plus_one_day.month, year=now_plus_one_day.year, hour=12, minute=0, second=0, microsecond=0, tzinfo=datetime.timezone(datetime.timedelta(hours=9))).astimezone(LOCAL_TZ)
    sound_conditions = [
        (genshin_note.current_resin >= 0.99 * genshin_note.max_resin, 10000),
        (genshin_note.current_resin >= 0.95 * genshin_note.max_resin, 1000),
        (genshin_note.current_resin >= 0.90 * genshin_note.max_resin, 3000),
        (genshin_note.current_realm_currency >= 0.99 * genshin_note.max_realm_currency, 10000),
        (genshin_note.current_realm_currency >= 0.95 * genshin_note.max_realm_currency, 1000),
        (genshin_note.current_realm_currency >= 0.90 * genshin_note.max_realm_currency, 3000),
        (zzz_note.battery_charge.current >= 0.99 * zzz_note.battery_charge.max, 10000),
        (zzz_note.battery_charge.current >= 0.95 * zzz_note.battery_charge.max, 1000),
        (zzz_note.battery_charge.current >= 0.90 * zzz_note.battery_charge.max, 3000),
        (genshin_note.daily_task.claimed_commission_reward != True and datetime_reset_hoyo_servers - now <= datetime.timedelta(hours=5), 15000),
        (zzz_note.engagement.current != zzz_note.engagement.max and datetime_reset_hoyo_servers - now <= datetime.timedelta(hours=5), 15000),
    ]

    for condition, frequency in sound_conditions:
        if condition:
            play_sound(frequency, 300, 5)
            break