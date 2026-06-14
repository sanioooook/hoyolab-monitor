import sys
import genshin
from genshin.client.manager.cookie import fetch_cookie_with_stoken_v2
from config import LANG, GENSHIN_UID, ZZZ_UID, HSR_UID, HOYOLAB_LOGIN, HOYOLAB_PASSWORD
from utils.cookies_manager import load_cookies, save_cookies


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
        await client.login_with_app_password(HOYOLAB_LOGIN, HOYOLAB_PASSWORD)
        print("[Client] Fetching ltoken_v2 and cookie_token_v2...")
        extra = await fetch_cookie_with_stoken_v2(
            client.cookie_manager.cookies,
            token_types=[2, 4],
        )
        client.set_cookies({**dict(client.cookie_manager.cookies), **extra})
        save_cookies(client)

    if GENSHIN_UID:
        client.uids[genshin.Game.GENSHIN] = GENSHIN_UID
    if ZZZ_UID:
        client.uids[genshin.Game.ZZZ] = ZZZ_UID
    if HSR_UID:
        client.uids[genshin.Game.STARRAIL] = HSR_UID
    return client