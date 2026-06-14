import os
from genshin.models import AppLoginResult
from config import COOKIE_FILE


def save_cookies_from_login_result(login_result: AppLoginResult) -> None:
    """Save login result cookies after login."""
    with open(COOKIE_FILE, "w", encoding="utf-8") as f:
        f.write(login_result.to_str())
    print(f"[Cookies] Saved to {COOKIE_FILE}")

def load_cookies() -> str | None:
    """Load cookies dict if exists."""
    if not os.path.exists(COOKIE_FILE):
        return None
    try:
        with open(COOKIE_FILE, "r", encoding="utf-8") as f:
            data = f.read()
        print(f"[Cookies] Loaded from {COOKIE_FILE}")
        return data
    except Exception as e:
        print(f"[Cookies] Failed to load: {e}")
        return None

def clear_cookies():
    """Delete saved cookies file (for re-login/reset)."""
    if os.path.exists(COOKIE_FILE):
        os.remove(COOKIE_FILE)
        print(f"[Cookies] Cleared {COOKIE_FILE}")