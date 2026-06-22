import datetime
import typing
from genshin.models import Notes, ZZZNotes, StarRailNote
from config import LOCAL_TZ
from utils.sound import play_sound


def check_and_play_sound(
    now: datetime.datetime,
    genshin_note: typing.Optional[Notes] = None,
    zzz_note: typing.Optional[ZZZNotes] = None,
    hsr_note: typing.Optional[StarRailNote] = None,
) -> None:
    now_plus_one_day = now + datetime.timedelta(days=1)
    reset_time = datetime.datetime(
        day=now_plus_one_day.day, month=now_plus_one_day.month, year=now_plus_one_day.year,
        hour=12, minute=0, second=0, microsecond=0,
        tzinfo=datetime.timezone(datetime.timedelta(hours=9)),
    ).astimezone(LOCAL_TZ)
    near_reset = reset_time - now <= datetime.timedelta(hours=5)

    sound_conditions = []

    if genshin_note is not None:
        sound_conditions += [
            (genshin_note.current_resin >= 0.99 * genshin_note.max_resin, 10000),
            (genshin_note.current_resin >= 0.95 * genshin_note.max_resin, 1000),
            (genshin_note.current_resin >= 0.90 * genshin_note.max_resin, 3000),
            (genshin_note.current_realm_currency >= 0.99 * genshin_note.max_realm_currency, 10000),
            (genshin_note.current_realm_currency >= 0.95 * genshin_note.max_realm_currency, 1000),
            (genshin_note.current_realm_currency >= 0.90 * genshin_note.max_realm_currency, 3000),
            (not genshin_note.daily_task.claimed_commission_reward and near_reset, 15000),
        ]

    if zzz_note is not None:
        sound_conditions += [
            (zzz_note.battery_charge.current >= 0.99 * zzz_note.battery_charge.max, 10000),
            (zzz_note.battery_charge.current >= 0.95 * zzz_note.battery_charge.max, 1000),
            (zzz_note.battery_charge.current >= 0.90 * zzz_note.battery_charge.max, 3000),
            (zzz_note.engagement.current != zzz_note.engagement.max and near_reset, 15000),
        ]

    if hsr_note is not None:
        sound_conditions += [
            (hsr_note.current_stamina >= 0.99 * hsr_note.max_stamina, 10000),
            (hsr_note.current_stamina >= 0.95 * hsr_note.max_stamina, 1000),
            (hsr_note.current_stamina >= 0.90 * hsr_note.max_stamina, 3000),
            (hsr_note.current_train_score < hsr_note.max_train_score and near_reset, 15000),
        ]

    for condition, frequency in sound_conditions:
        if condition:
            play_sound(frequency, 300, 5)
            break