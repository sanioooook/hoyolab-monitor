from genshin.models import Notes, AttendanceRewardStatus, HardChallenge, ImgTheater, SpiralAbyss
from .shared_format import *
from config import LOCAL_TZ, HOYO_TZ


def format_genshin(genshin_note: Notes,
                   genshin_spiral_abyss: SpiralAbyss,
                   genshin_imaginarium_theater: ImgTheater,
                   stygian_onslaught: list[HardChallenge],
                   now: datetime.datetime) -> str :
    return f"""Genshin:
{format_genshin_notes(genshin_note, now)}
{format_genshin_theater(genshin_imaginarium_theater, now)}
{format_genshin_abyss(genshin_spiral_abyss, now)}
{format_genshin_stygian_onslaught(stygian_onslaught, now)}"""


def format_genshin_notes(genshin_note: Notes, now: datetime.datetime) -> str:
    if genshin_note is None:
        return f"Заметки в реальном времени | {red('Данных нет')}"
    expeditions_str = ""
    for expedition in genshin_note.expeditions:
        if expedition.remaining_time > datetime.timedelta(0):
            remaining = f"{expedition.remaining_time} осталось"
            completion_time = (
                f"Завершится {format_datetime(expedition.completion_time, now)}"
            )
            expeditions_str += f" - Продолжается | {remaining} | {completion_time}\n"
        else:
            expeditions_str += f" - Завершена\n"

    remained_resin_recovery_time = genshin_note.resin_recovery_time.astimezone(LOCAL_TZ) - now
    remained_realm_currency_recovery_time = (genshin_note.realm_currency_recovery_time.astimezone(LOCAL_TZ) - now)
    remained_transformer_recovery_recovery_time = (
                genshin_note.transformer_recovery_time.astimezone(LOCAL_TZ) - now)
    resin_discounts = genshin_note.max_resin_discounts - genshin_note.remaining_resin_discounts

    resin_text = f"{color_by_condition_for_resin(genshin_note.current_resin, genshin_note.max_resin)}/{genshin_note.max_resin}"
    realm_currency_text = f"{color_by_condition_for_resin(genshin_note.current_realm_currency, genshin_note.max_realm_currency)}/{genshin_note.max_realm_currency}"
    resin_recovery_time = format_datetime(genshin_note.resin_recovery_time, now, text_if_dt_is_none="Заполнено")
    realm_currency_recovery_time = format_datetime(genshin_note.realm_currency_recovery_time, now,
                                                   text_if_dt_is_none="Заполнено")
    resin_remained_time = format_timedelta(remained_resin_recovery_time)
    realm_currency_remained_time = format_timedelta(remained_realm_currency_recovery_time)
    transformer_recovery_remained_time = format_timedelta(remained_transformer_recovery_recovery_time)

    attendance_rewards_str = ""
    for index, attendance_reward in enumerate(genshin_note.daily_task.attendance_rewards):
        isLast = index == (len(genshin_note.daily_task.attendance_rewards) - 1)
        endLine = "" if isLast else " | "
        match attendance_reward.status:
            case AttendanceRewardStatus.AVAILABLE:
                attendance_rewards_str += yellow(f"{attendance_reward.progress}% Не забрано{endLine}")
            case AttendanceRewardStatus.COLLECTED:
                attendance_rewards_str += green(f"{attendance_reward.progress}% Забрано{endLine}")
            case AttendanceRewardStatus.FORBIDDEN:
                attendance_rewards_str += red(f"{attendance_reward.progress}% FORBIDDEN{endLine}")
            case AttendanceRewardStatus.UNAVAILABLE:
                attendance_rewards_str += red(f"{attendance_reward.progress}% Не заполнено{endLine}")
    stored_attendance_str = f"{genshin_note.daily_task.stored_attendance}"
    if genshin_note.daily_task.stored_attendance_refresh_countdown != None:
        stored_attendance_refresh_countdown = genshin_note.daily_task.stored_attendance_refresh_countdown
        remained_attendance_time = format_timedelta(stored_attendance_refresh_countdown)
        reset_datetime_attendance = stored_attendance_refresh_countdown + now
        reset_datetime_attendance_srt = format_datetime(reset_datetime_attendance, now, text_if_dt_is_none="Нет данных")
        stored_attendance_str += f" | Дата сброса {reset_datetime_attendance_srt} | Осталось времени {remained_attendance_time}"

    commissions_text = f"{color_by_condition(genshin_note.completed_commissions, genshin_note.max_commissions)}/{genshin_note.max_commissions}"
    commissions_reward = (
        " | " + red("[X] Haven\'t claimed rewards")
        if genshin_note.completed_commissions == genshin_note.max_commissions
           and not genshin_note.claimed_commission_reward
        else ""
    )

    resin_discounts_text = f"{color_by_condition(resin_discounts, genshin_note.max_resin_discounts)}/{genshin_note.max_resin_discounts}"
    transformer_text = format_datetime(genshin_note.transformer_recovery_time, now, text_if_dt_is_none="Откат завершен")

    return_str = f"""Первородная смола: {resin_text} | Заполнится {resin_recovery_time} | Осталось времени {resin_remained_time}
Сокровища обители: {realm_currency_text} | Заполнится {realm_currency_recovery_time} | Осталось времени {realm_currency_remained_time}
Поручения: {commissions_text}{commissions_reward}
Долгосрочные очки обучения: {stored_attendance_str}
    {attendance_rewards_str}
Враги, достойные упоминания: {resin_discounts_text}
Параметрический преобразователь: {transformer_text}
Экспедиции: {len(genshin_note.expeditions)}/{genshin_note.max_expeditions}
{expeditions_str}"""
    return return_str


def format_genshin_abyss(genshin_spiral_abyss: SpiralAbyss, now: datetime.datetime) -> str:
    if genshin_spiral_abyss is None:
        return red("Витая бездна | Данных нет")
    spiral_abyss_end_time = genshin_spiral_abyss.end_time.replace(tzinfo=LOCAL_TZ)
    spiral_abyss_end_time_text = format_datetime(spiral_abyss_end_time, now, text_if_dt_is_none="Завершено")
    remained_abyss_end_time = spiral_abyss_end_time - now
    max_floor = (
        green(genshin_spiral_abyss.max_floor)
        if genshin_spiral_abyss.max_floor == "12-3"
        else red(genshin_spiral_abyss.max_floor)
    )

    max_stars = 36
    total_stars = color_by_condition(genshin_spiral_abyss.total_stars, max_stars)
    return_str = f"""Витая бездна         | Закончится {spiral_abyss_end_time_text} | Осталось времени {format_timedelta(remained_abyss_end_time)}
    Общее количество звезд: {total_stars}/{max_stars} | Максимальный этаж {max_floor}"""
    return return_str


def format_genshin_theater(genshin_imaginarium_theater: ImgTheater, now: datetime.datetime) -> str:
    if genshin_imaginarium_theater is None:
        return red("Театр «Воображариум» | Данных нет")

    current_imaginarium_theater = genshin_imaginarium_theater.datas[0]
    # timestapm = current_imaginarium_theater.schedule.end_time
    current_imaginarium_theater_end_time = (
        datetime.datetime.fromtimestamp(current_imaginarium_theater.schedule.end_time)
        .replace(tzinfo=HOYO_TZ).astimezone(LOCAL_TZ))
    imaginarium_theater_end_time_text = format_datetime(current_imaginarium_theater_end_time, now,
                                                        text_if_dt_is_none="Завершено")
    remained_imaginarium_theater_end_time = current_imaginarium_theater_end_time - now

    finished_acts = list(
        filter(lambda act: act.finish_datetime is not None, current_imaginarium_theater.acts)).__len__()
    max_acts = 12
    total_acts = color_by_condition(finished_acts, max_acts)
    return_str = f"""Театр «Воображариум» | Закончится {imaginarium_theater_end_time_text} | Осталось времени {format_timedelta(remained_imaginarium_theater_end_time)}
    Общее количество актов: {total_acts}/{max_acts}"""
    return return_str


def format_genshin_stygian_onslaught(stygian_onslaught: list[HardChallenge],
                                     now: datetime.datetime) -> str:
    if stygian_onslaught is None or stygian_onslaught[0] is None:
        return red("Мрачный натиск | Данных нет")
    current_stygian_onslaught = stygian_onslaught[0].season
    current_stygian_onslaught_end_time = current_stygian_onslaught.end_at.replace(tzinfo=HOYO_TZ)
    stygian_onslaught_end_time_text = format_datetime(current_stygian_onslaught_end_time, now,
                                                      text_if_dt_is_none="Завершено")
    remained_stygian_onslaught_end_time = current_stygian_onslaught_end_time - now

    single_best = stygian_onslaught[0].single_player.best_record
    multi_best = stygian_onslaught[0].multi_player.best_record

    best = None
    mode = ""
    max_difficulty = 6

    if single_best and multi_best:
        # look on difficulty
        if single_best.difficulty > multi_best.difficulty:
            best, mode = single_best, "Соло"
        elif single_best.difficulty < multi_best.difficulty:
            best, mode = multi_best, "Кооператив"
        else:
            # if difficulty is same - look on time (less = coolest)
            if single_best.time_used <= multi_best.time_used:
                best, mode = single_best, "Соло"
            else:
                best, mode = multi_best, "Кооператив"
    elif single_best:
        best, mode = single_best, "Соло"
    elif multi_best:
        best, mode = multi_best, "Кооператив"

    if best is None:
        record_text = red("Данных нет")
    else:
        record_text = f"{mode} | Сложность: {color_by_condition(best.difficulty, max_difficulty)}/{max_difficulty} | Время: {best.time_used} сек"

    return_str = f"""Мрачный натиск       | Закончится {stygian_onslaught_end_time_text} | Осталось времени {format_timedelta(remained_stygian_onslaught_end_time)}
    Лучший результат: {record_text}"""
    return return_str
