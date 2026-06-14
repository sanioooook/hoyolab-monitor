from typing import Optional

from colorama import Fore, Style
import datetime
from config import LOCAL_TZ

FORMAT = "%d.%m.%Y %H:%M:%S"


def color_text(text: str, color: str) -> str:
    return f"{color}{text}{Style.RESET_ALL}"

def red(text: str) -> str:
    return color_text(text, Fore.RED)

def green(text: str) -> str:
    return color_text(text, Fore.GREEN)

def cyan(text: str) -> str:
    return color_text(text, Fore.CYAN)

def yellow(text: str) -> str:
    return color_text(text, Fore.YELLOW)

def color_by_condition(current: int, max_value: int) -> str:
    if current >= max_value:
        return green(str(current))
    elif current == 0:
        return red(str(current))
    else:
        return yellow(str(current))

def color_by_condition_revert(current: int, max_value: int) -> str:
    if current >= max_value:
        return red(str(current))
    elif current == 0:
        return green(str(current))
    else:
        return yellow(str(current))

def color_by_condition_for_resin(current: int, max_value: int) -> str:
    if current >= max_value:
        return red(str(current))
    elif current <= int((max_value)*0.5):
        return green(str(current))
    else:
        return yellow(str(current))

def format_timedelta(td: datetime.timedelta):
    if td.total_seconds() < 0:
        td = datetime.timedelta(0)

    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours >= 21 or days != 0:
        color = Fore.GREEN
    elif hours < 3 and days == 0:
        color = Fore.RED
    elif 3 <= hours <= 21 and days == 0:
        color = Fore.YELLOW
    else:
        color = Style.RESET_ALL

    return f"{color}{days} дней, {hours:02}:{minutes:02}:{seconds:02}{Style.RESET_ALL}"

def format_datetime(dt: datetime.datetime, now: datetime.datetime, deadline_days = 2, deadline_hours = 12, text_if_dt_is_none = "Завершено", to_local_timezone = True):
    if(dt is None):
        return red(text_if_dt_is_none)
    if(to_local_timezone):
        dt = dt.astimezone(LOCAL_TZ)
    formatted_time = str(dt.strftime(FORMAT))
    if (dt > now):
        if(dt - now >= datetime.timedelta(days=deadline_days, hours=deadline_hours)):
            return green(formatted_time)
        else:
            return yellow(formatted_time)
    else:
        return red(formatted_time)


def _color_rating(rating: Optional[str]) -> str:
    # rating: "S", "A", "B", "S+", or None
    if rating == "S+":
        return cyan(rating)
    if rating == "S":
        return green(rating)
    if rating == "A":
        return yellow(rating)
    if rating == "B":
        return red(rating)
    return red("Данных нет")
