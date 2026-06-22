from typing import Sequence

from genshin.models import DeadlyAssault, ZZZUserStats, ShiyuDefense, ZZZNotes, ShiyuDefenseV2
from genshin.models.zzz.chronicle.challenge import ShiyuV2FifthFloorLayer

from .shared_format import *
from config import LOCAL_TZ, HOYO_TZ
from .shared_format import _color_rating
import re

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def _visible_len(text: str) -> int:
    # Strip ANSI escape sequences to compute real on-screen width
    return len(_ANSI_RE.sub("", text))


def _pad_right(text: str, width: int) -> str:
    # Pad based on visible length (ANSI codes ignored)
    pad = width - _visible_len(text)
    return text + (" " * pad if pad > 0 else "")


def _color_score(score: Optional[int], rating: Optional[str]) -> str:
    if score is None:
        return red("Данных нет")
    if rating == "S+":
        return cyan(str(score))
    if rating == "S":
        return green(str(score))
    if rating == "A":
        return yellow(str(score))
    if rating == "B":
        return red(str(score))
    return red(str(score))


def _is_layer_passed(layer: Optional[ShiyuV2FifthFloorLayer]) -> bool:
    if layer is None:
        return False
    # Practical heuristic: if score > 0 or clear_time > 0 we consider it completed
    score = getattr(layer, "score", 0) or 0
    clear_time = getattr(layer, "clear_time", 0) or 0
    return score > 0 or clear_time > 0


def format_deadly_assault(deadly_assault: DeadlyAssault, now: datetime.datetime) -> str:
    if deadly_assault is not None:
        end_time = (deadly_assault.end_time.replace(tzinfo=HOYO_TZ).astimezone(LOCAL_TZ)
                    if deadly_assault.end_time is not None
                    else None)
        deadly_assault_remained_time = (format_timedelta(end_time - now)
                                        if end_time is not None
                                        else red("Данных нет"))
        deadly_assault_end_time = (format_datetime(end_time, now, to_local_timezone=False)
                                   if end_time is not None
                                   else red("Данных нет"))
        deadly_assault_str = f"Опасный штурм | Закончится {deadly_assault_end_time} | Осталось времени {deadly_assault_remained_time}"
        if deadly_assault.has_data:
            max_stars = len(deadly_assault.challenges) * 3
            total_star = deadly_assault.total_star
            deadly_assault_str = deadly_assault_str + f"""
    Полученные звезды: {color_by_condition(total_star, max_stars)}/{max_stars}
    Количество очков: {deadly_assault.total_score} | Ранг {deadly_assault.rank_percent}"""
        else:
            deadly_assault_str = deadly_assault_str + "\n    " + red("Данных нет")
        return deadly_assault_str
    return red("Опасный штурм | Данных нет")


def format_ZZZ_stats(zzz_stats: ZZZUserStats, now: datetime.datetime) -> str:
    if zzz_stats is not None:
        zzz_stats_str = ""
        if zzz_stats.cat_notes is not None:
            total_sum = sum(item.total for item in zzz_stats.cat_notes)
            num_sum = sum(item.num for item in zzz_stats.cat_notes)
            min_num_item = min((item for item in zzz_stats.cat_notes if item.num != item.total), key=lambda x: x.num,
                               default=None)
            min_num_name = min_num_item.name if min_num_item else None
            if total_sum != num_sum:
                zzz_stats_str = f"\nМедали инспектора Мяучело: {color_by_condition(num_sum, total_sum)}/{total_sum} | {yellow(min_num_name)}: {yellow(str(min_num_item.num))}/{min_num_item.total}"
        return zzz_stats_str
    return ""


def format_shiyu_defense(shiyu_defense: ShiyuDefenseV2, now: datetime.datetime) -> str:
    if shiyu_defense is None:
        return red("Оборона Шиюй | Данных нет")

    end_time = (shiyu_defense.end_time.replace(tzinfo=HOYO_TZ).astimezone(LOCAL_TZ)
                if shiyu_defense.end_time is not None
                else None)
    shiyu_defense_remained_time = (format_timedelta(end_time - now)
                                   if end_time is not None
                                   else red("Данных нет"))
    shiyu_defense_end_time = (format_datetime(end_time, now, to_local_timezone=False)
                              if end_time is not None
                              else red("Данных нет"))
    shiyu: list[str] = [
        f"Оборона Шиюй | Закончится {shiyu_defense_end_time} | Осталось времени {shiyu_defense_remained_time}"
    ]

    fourth = shiyu_defense.fourth_frontier
    fourth_passed = fourth is not None
    if fourth_passed:
        fourth_rating = _color_rating(getattr(fourth, "rating", None))
        shiyu.append(f"4я линия: {green('пройдена')} | Рейтинг: {fourth_rating}")
    else:
        shiyu.append(f"4я линия: {red('не пройдена')}")

    brief = shiyu_defense.brief_info
    brief_rating = brief.rating if brief else None
    if brief_rating:
        shiyu.append(
            f"5я линия (итог): Рейтинг {_color_rating(brief_rating)} | Очки (текущие) {_color_score(brief.score, brief_rating)}")
    else:
        shiyu.append(f"5я линия (итог): {red('не пройдена')}")

    # 5th line layers table (3 columns)
    layers: Sequence[ShiyuV2FifthFloorLayer] = []
    if shiyu_defense.fifth_frontier and getattr(shiyu_defense.fifth_frontier, "layers", None):
        layers = list(shiyu_defense.fifth_frontier.layers)

    # Normalize to exactly 3 entries
    cols: list[Optional[ShiyuV2FifthFloorLayer]] = []
    for i in range(3):
        cols.append(layers[i] if i < len(layers) else None)

    headers = [f"5я линия {i + 1}" for i in range(3)]

    rating_cells: list[str] = []
    score_cells: list[str] = []

    for col in cols:
        if not _is_layer_passed(col):
            rating_cells.append(f"рейтинг - {red('Данных нет')}")
            score_cells.append(f"очки - {red('Данных нет')}")
            continue

        r = getattr(col, "rating", None)
        score = getattr(col, "score", None)

        rating_cells.append(f"рейтинг - {_color_rating(r)}")
        score_cells.append(f"очки - {_color_score(score, r)}")

    # Compute per-column widths by max visible length across header/rating/score
    widths: list[int] = []
    for i in range(3):
        w = max(
            _visible_len(headers[i]),
            _visible_len(rating_cells[i]),
            _visible_len(score_cells[i]),
        )
        widths.append(w)

    sep = " | "

    header_row = sep.join(_pad_right(headers[i], widths[i]) for i in range(3))
    ratings_row = sep.join(_pad_right(rating_cells[i], widths[i]) for i in range(3))
    scores_row = sep.join(_pad_right(score_cells[i], widths[i]) for i in range(3))

    shiyu.append(header_row)
    shiyu.append(ratings_row)
    shiyu.append(scores_row)

    return "\n".join(shiyu)


def format_ZZZ_notes(zzz_note: ZZZNotes, now: datetime.datetime) -> str:
    if zzz_note is not None:
        buttery_charge = zzz_note.battery_charge
        scratch_card_completed = zzz_note.scratch_card_completed
        engagement = zzz_note.engagement
        tasks_text = red("Данных нет")
        task_reset_datetime = red("Данных нет")
        task_remained_time = red("Данных нет")
        if zzz_note.weekly_task is not None:
            tasks = zzz_note.weekly_task
            tasks_text = f"{color_by_condition(tasks.cur_point, tasks.max_point)}/{tasks.max_point}"
            task_reset_datetime = format_datetime(tasks.reset_datetime, now, deadline_days=1, deadline_hours=0)
            task_remained_time = format_timedelta(tasks.refresh_time)

        remained_buttery_charge_time = buttery_charge.full_datetime - now
        hollow_zero = zzz_note.hollow_zero

        video_store_state_mapping = {
            "SaleStateDone": red("Доступен расчёт"),
            "SaleStateDoing": green("Уже открыт"),
            "SaleStateNo": yellow("Ожидается открытие"),
        }
        video_store_state_str = video_store_state_mapping.get(
            zzz_note.video_store_state.value, ""
        )

        battery_charge_text = (color_by_condition_for_resin(buttery_charge.current,
                                                            buttery_charge.max)) + f"/{buttery_charge.max}"
        battery_charge_time = format_datetime(buttery_charge.full_datetime, now, deadline_days=1, deadline_hours=0)
        battery_remained_time = format_timedelta(remained_buttery_charge_time)

        engagement_text = f"{color_by_condition(engagement.current, engagement.max)}/{engagement.max}"

        scratch_card_text = (
            green("Выполнено") if scratch_card_completed else red("Не выполнено")
        )

        bounty_commission = hollow_zero.bounty_commission
        bounty_commission_text = (
            f"{color_by_condition(bounty_commission.cur_completed, bounty_commission.total)}/{bounty_commission.total}"
        )
        hollow_zero_reset_datetime = format_datetime(hollow_zero.bounty_commission.reset_datetime, now)
        hollow_zero_remained_time = format_timedelta(hollow_zero.bounty_commission.refresh_time)

        return_str = f"""Заряд аккумуляторов: {battery_charge_text} | Заполнится {battery_charge_time} | Осталось времени {battery_remained_time}
Управление видеопрокатом: {video_store_state_str}
Текущая активность: {engagement_text}
Бинго Риду: {tasks_text} | Сбросится {task_reset_datetime} | Осталось времени {task_remained_time}
Счастливый билет: {scratch_card_text}
Нулевая каверна | Сбросится {hollow_zero_reset_datetime} | Осталось времени {hollow_zero_remained_time}
    Призовые заказы: {bounty_commission_text}"""
    else:
        return_str = f"Заметки в реальном времени | {red('Данных нет')}"
    return return_str


def format_ZZZ_temple(zzz_note: ZZZNotes, now: datetime.datetime) -> str:
    if zzz_note is None or zzz_note.temple_running is None:
        return_str = f"Храм Суйбань | {red('Данных нет')}"
    else:
        zzz_note_temple_running = zzz_note.temple_running
        expedition_state = zzz_note_temple_running.expedition_state
        shelve_state = zzz_note_temple_running.shelve_state
        bench_state = zzz_note_temple_running.bench_state
        current_currency = zzz_note_temple_running.current_currency
        currency_reset_datetime = zzz_note_temple_running.reset_datetime
        level = zzz_note_temple_running.level
        weekly_currency_max = zzz_note_temple_running.weekly_currency_max
        max_level = 45

        currency_text = f"{color_by_condition(current_currency, weekly_currency_max)}/{weekly_currency_max}"
        currency_reset_datetime = format_datetime(currency_reset_datetime, now, deadline_days=2, deadline_hours=0)
        level_text = f"{color_by_condition(level, max_level)}/{max_level}"
        return_str = f"Тунбао: {currency_text} | Сброс {currency_reset_datetime}"

        auto_work = zzz_note_temple_running.auto_work
        if auto_work is not None:
            if auto_work.is_auto_work_running and auto_work.auto_work_ended is False:
                auto_work_status = green("В процессе")
            else:
                auto_work_status = red("Доступна выручка")
            auto_work_end_time = format_timedelta(auto_work.left_ts)
            auto_work_end_datetime = format_datetime(now + auto_work.left_ts, now, deadline_days=0, deadline_hours=3)
            return_str += f"\n    Уровень: {level_text} | Авторежим: {auto_work_status} | Остановится {auto_work_end_datetime} | Осталось времени: {auto_work_end_time}"
        else:
            expedition_state_mapping = {
                "ExpeditionStateInCanSend": yellow("Можно отправить"),
                "ExpeditionStateInProgress": green("Отряд в пути"),
                "ExpeditionStateEnd": red("Отряд вернулся"),
            }
            expedition_state_str = expedition_state_mapping.get(
                expedition_state.value, ""
            )

            bench_state_mapping = {
                "BenchStateCanProduce": red("Можно изготовить"),
                "BenchStateProducing": green("Идёт изготовление"),
            }
            bench_state_str = bench_state_mapping.get(
                bench_state.value, ""
            )

            shelve_state_mapping = {
                "ShelveStateCanSell": red("Готово к продаже"),
                "ShelveStateSelling": green("Идёт продажа"),
                "ShelveStateSoldOut": yellow("Нет товаров"),
            }
            shelve_state_str = shelve_state_mapping.get(
                shelve_state.value, ""
            )

            return_str += f"\tУровень: {level_text} | Экспедиции: {expedition_state_str} | Изготовление: {bench_state_str} | Торговля: {shelve_state_str}"
    return return_str
