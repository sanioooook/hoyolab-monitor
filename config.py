import os
import pathlib
import datetime
import tzlocal

_ROOT = pathlib.Path(__file__).parent

def load_env():
    filepath = _ROOT / ".env"
    if not filepath.exists():
        print(f"[Config] .env not found at {filepath} — copy .env.example and fill in your credentials")
        return
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ[key] = value

load_env()

# Timezones
LOCAL_TZ = tzlocal.get_localzone()
HOYO_TZ = datetime.timezone(datetime.timedelta(hours=1))

# Environment vars
LANG = os.getenv("LANG", "en-us")
TWOCAPTCHA_API_KEY = os.getenv("TWOCAPTCHA_API_KEY")

def _optional_int(key: str):
    v = os.getenv(key)
    return int(v) if v else None

GENSHIN_UID = _optional_int("GENSHIN_UID")
ZZZ_UID     = _optional_int("ZZZ_UID")
HSR_UID     = _optional_int("HSR_UID")
DELAY = int(os.getenv("DELAY_MINUTES", "15")) * 60
HOYOLAB_LOGIN = os.getenv("HOYOLAB_LOGIN")
HOYOLAB_PASSWORD = os.getenv("HOYOLAB_PASSWORD")
COOKIE_FILE = str(_ROOT / "cookies.txt")
