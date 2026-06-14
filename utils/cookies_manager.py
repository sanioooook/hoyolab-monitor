import os
import json
import genshin
from config import COOKIE_FILE


def save_cookies(client: genshin.Client) -> None:
    cookies = dict(client.cookie_manager.cookies)
    with open(COOKIE_FILE, "w", encoding="utf-8") as f:
        json.dump(cookies, f, indent=2)
    print(f"[Cookies] Saved to {COOKIE_FILE}")


def load_cookies() -> dict | None:
    if not os.path.exists(COOKIE_FILE):
        return None
    try:
        with open(COOKIE_FILE, "r", encoding="utf-8") as f:
            data = f.read().strip()
        # Support old format: "key=value; key2=value2"
        if data.startswith("{"):
            cookies = json.loads(data)
        else:
            cookies = dict(p.strip().split("=", 1) for p in data.split(";") if "=" in p)
        print(f"[Cookies] Loaded from {COOKIE_FILE}")
        return cookies
    except Exception as e:
        print(f"[Cookies] Failed to load: {e}")
        return None


def clear_cookies():
    if os.path.exists(COOKIE_FILE):
        os.remove(COOKIE_FILE)
        print(f"[Cookies] Cleared {COOKIE_FILE}")