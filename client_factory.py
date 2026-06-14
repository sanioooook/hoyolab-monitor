import sys
import genshin
from config import LANG, GENSHIN_UID, ZZZ_UID, HSR_UID, HOYOLAB_LOGIN, HOYOLAB_PASSWORD
from utils.cookies_manager import load_cookies, save_cookies_from_login_result


async def create_client() -> genshin.Client:
    client = genshin.Client(lang=LANG)
    cookies = load_cookies()
    if cookies:
        client.set_cookies(cookies)
        print("[Client] Using stored cookies.")
    else:
        if not HOYOLAB_LOGIN or not HOYOLAB_PASSWORD:
            print("[Error] HOYOLAB_LOGIN and HOYOLAB_PASSWORD are not set in .env")
            sys.exit(1)
        print("[Client] No cookies found, logging in...")
        result = await client.login_with_app_password(HOYOLAB_LOGIN, HOYOLAB_PASSWORD)
        save_cookies_from_login_result(result)

    if GENSHIN_UID:
        client.uids[genshin.Game.GENSHIN] = GENSHIN_UID
    if ZZZ_UID:
        client.uids[genshin.Game.ZZZ] = ZZZ_UID
    if HSR_UID:
        client.uids[genshin.Game.STARRAIL] = HSR_UID
    return client