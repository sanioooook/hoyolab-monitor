import urllib.request
import json
from colorama import Fore, Style
from version import GITHUB_REPO

GITHUB_API = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"


def _parse_version(v: str) -> tuple[int, ...]:
    return tuple(int(x) for x in v.lstrip("v").split("."))


def check_for_updates(current_version: str) -> None:
    try:
        req = urllib.request.Request(GITHUB_API, headers={"User-Agent": "hoyolab-monitor"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())

        latest = data.get("tag_name", "").lstrip("v")
        if not latest:
            return

        if _parse_version(latest) > _parse_version(current_version):
            url = data.get("html_url", "")
            print(
                f"{Fore.YELLOW}[Обновление] Доступна версия {latest} "
                f"(текущая: {current_version}){Style.RESET_ALL}"
            )
            if url:
                print(f"{Fore.YELLOW}  Скачать: {url}{Style.RESET_ALL}")
            print()
    except Exception:
        pass
