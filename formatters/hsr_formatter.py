import datetime

from genshin.models import StarRailNote, AnomalyArbitration, StarRailAPCShadow, StarRailPureFiction, StarRailChallenge

from .shared_format import *
from config import LOCAL_TZ


def format_hsr_notes(hsr_note: StarRailNote, now: datetime.datetime) -> str:
    if hsr_note is None:
        return ""

    expeditions_str = ""
    for expedition in hsr_note.expeditions:
        if expedition.finished:
            expeditions_str += f" - {expedition.name} | {red('Завершена')}\n"
        else:
            remaining = format_timedelta(expedition.remaining_time)
            completion = format_datetime(expedition.completion_time, now)
            expeditions_str += f" - {expedition.name} | {remaining} осталось | Завершится {completion}\n"

    stamina_text = f"{color_by_condition_for_resin(hsr_note.current_stamina, hsr_note.max_stamina)}/{hsr_note.max_stamina}"
    stamina_fill_at = format_datetime(hsr_note.stamina_recovery_time, now, text_if_dt_is_none="Заполнено")
    stamina_remains = format_timedelta(hsr_note.stamina_recover_time)

    if hsr_note.is_reserve_stamina_full:
        reserve_text = f"{red(str(hsr_note.current_reserve_stamina))}/2400"
    elif hsr_note.current_reserve_stamina > 0:
        reserve_text = f"{yellow(str(hsr_note.current_reserve_stamina))}/2400"
    else:
        reserve_text = f"{hsr_note.current_reserve_stamina}/2400"

    training_text = f"{color_by_condition(hsr_note.current_train_score, hsr_note.max_train_score)}/{hsr_note.max_train_score}"
    rogue_text = f"{color_by_condition(hsr_note.current_rogue_score, hsr_note.max_rogue_score)}/{hsr_note.max_rogue_score}"
    echo_of_war_text = f"{color_by_condition_revert(hsr_note.remaining_weekly_discounts, hsr_note.max_weekly_discounts)}/{hsr_note.max_weekly_discounts}"
    sync_points_text = f"{color_by_condition_revert(hsr_note.current_bonus_synchronicity_points, hsr_note.max_bonus_synchronicity_points)}/{hsr_note.max_bonus_synchronicity_points}"

    return (
        f"TB Power: {stamina_text} | Заполнится {stamina_fill_at} | Осталось времени {stamina_remains}\n"
        f"Reserved TB Power: {reserve_text}\n"
        f"Daily Training: {training_text}\n"
        f"Simulated Universe: {rogue_text}\n"
        f"Echo of War: {echo_of_war_text}\n"
        f"Bonus Synchronicity Points: {sync_points_text}\n"
        f"Assignments: {hsr_note.accepted_expedition_num}/{hsr_note.total_expedition_num}\n"
        f"{expeditions_str}"
    )


def format_hsr_anomaly_arbitration(data: AnomalyArbitration, now: datetime.datetime) -> str:
    if data is None:
        return ""

    mini_boss_max = 9
    boss_max = 3
    mini_boss_text = f"{color_by_condition(data.summary.mini_boss_stars, mini_boss_max)}/{mini_boss_max}"
    boss_text = f"{color_by_condition(data.summary.boss_stars, boss_max)}/{boss_max}"

    end_dt = data.records[0].season.end_time.datetime.replace(tzinfo=LOCAL_TZ)
    end_text = format_datetime(end_dt, now, to_local_timezone=False)
    remains = format_timedelta(end_dt - now)
    name = data.records[0].season.name

    return f"Арбитраж аномалий·{name}: Мини-босс: {mini_boss_text} | Босс: {boss_text} | Закончится {end_text} | Осталось времени {remains}"


def format_hsr_apocalyptic_shadow(data: StarRailAPCShadow, now: datetime.datetime) -> str:
    if data is None or not data.has_data:
        return ""

    stars_max = 12
    stars_text = f"{color_by_condition(data.total_stars, stars_max)}/{stars_max}"

    end_dt = data.seasons[0].end_time.datetime.replace(tzinfo=LOCAL_TZ)
    end_text = format_datetime(end_dt, now, to_local_timezone=False)
    remains = format_timedelta(end_dt - now)

    return f"Иллюзия конца·{data.seasons[0].name}: {stars_text} | Закончится {end_text} | Осталось времени {remains}"


def format_hsr_pure_fiction(data: StarRailPureFiction, now: datetime.datetime) -> str:
    if data is None or not data.has_data:
        return ""

    stars_max = 12
    stars_text = f"{color_by_condition(data.total_stars, stars_max)}/{stars_max}"

    end_dt = data.seasons[0].end_time.datetime.replace(tzinfo=LOCAL_TZ)
    end_text = format_datetime(end_dt, now, to_local_timezone=False)
    remains = format_timedelta(end_dt - now)

    return f"Чистый вымысел·{data.seasons[0].name}: {stars_text} | Закончится {end_text} | Осталось времени {remains}"


def format_hsr_challenge(data: StarRailChallenge, now: datetime.datetime) -> str:
    if data is None or not data.has_data:
        return ""

    stars_max = 36
    stars_text = f"{color_by_condition(data.total_stars, stars_max)}/{stars_max}"

    end_dt = data.seasons[0].end_time.datetime.replace(tzinfo=LOCAL_TZ)
    end_text = format_datetime(end_dt, now, to_local_timezone=False)
    remains = format_timedelta(end_dt - now)

    return f"Зал забвения·{data.seasons[0].name}: {stars_text} | Закончится {end_text} | Осталось времени {remains}"
