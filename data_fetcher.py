import genshin
import asyncio
from genshin.models import (
    ImgTheater, HardChallenge, SpiralAbyss, Notes, DeadlyAssault, ShiyuDefense,
    ZZZUserStats, ZZZNotes, StarRailNote, AnomalyArbitration, StarRailAPCShadow,
    StarRailPureFiction, StarRailChallenge,
)
from utils.decorators import handle_geetest
from config import LANG, GENSHIN_UID, ZZZ_UID, HSR_UID


async def update_characters():
    try:
        await genshin.utility.update_characters_enka(['en-us', LANG])
    except Exception as e:
        print(e)


@handle_geetest
async def zzz_notes(client: genshin.Client) -> ZZZNotes | None:
    try:
        return await client.get_zzz_notes()
    except Exception as e:
        print(e)
    return None


@handle_geetest
async def zzz_user(client: genshin.Client) -> ZZZUserStats | None:
    try:
        return await client.get_zzz_user()
    except Exception as e:
        print(e)
    return None


@handle_geetest
async def get_shiyu_defense(client: genshin.Client) -> ShiyuDefense | None:
    try:
        return await client.get_shiyu_defense()
    except Exception as e:
        print(e)
    return None


@handle_geetest
async def get_deadly_assault(client: genshin.Client) -> DeadlyAssault | None:
    try:
        return await client.get_deadly_assault()
    except Exception as e:
        print(e)
    return None


@handle_geetest
async def genshin_notes(client: genshin.Client) -> Notes | None:
    try:
        return await client.get_genshin_notes()
    except Exception as e:
        print(e)
    return None


@handle_geetest
async def genshin_abyss(client: genshin.Client) -> SpiralAbyss | None:
    try:
        return await client.get_genshin_spiral_abyss(lang=LANG)
    except Exception as e:
        print(e)
    return None


@handle_geetest
async def stygian_onslaught(client: genshin.Client) -> list[HardChallenge] | None:
    try:
        return await client.get_stygian_onslaught()
    except Exception as e:
        print(e)
    return None


@handle_geetest
async def genshin_imaginarium_theater(client: genshin.Client) -> ImgTheater | None:
    try:
        return await client.get_imaginarium_theater()
    except Exception as e:
        print(e)
    return None


@handle_geetest
async def hsr_notes(client: genshin.Client) -> StarRailNote | None:
    try:
        return await client.get_starrail_notes()
    except Exception as e:
        print(e)
    return None


@handle_geetest
async def hsr_anomaly_arbitration(client: genshin.Client) -> AnomalyArbitration | None:
    try:
        return await client.get_anomaly_arbitration()
    except Exception as e:
        print(e)
    return None


@handle_geetest
async def hsr_apocalyptic_shadow(client: genshin.Client) -> StarRailAPCShadow | None:
    try:
        return await client.get_apocalyptic_shadow()
    except Exception as e:
        print(e)
    return None


@handle_geetest
async def hsr_pure_fiction(client: genshin.Client) -> StarRailPureFiction | None:
    try:
        return await client.get_starrail_pure_fiction()
    except Exception as e:
        print(e)
    return None


@handle_geetest
async def hsr_challenge(client: genshin.Client) -> StarRailChallenge | None:
    try:
        return await client.get_starrail_challenge()
    except Exception as e:
        print(e)
    return None


async def _skip():
    return None


async def collect_data(client):
    return await asyncio.gather(
        genshin_notes(client)      if GENSHIN_UID else _skip(),
        zzz_notes(client)          if ZZZ_UID     else _skip(),
        zzz_user(client)           if ZZZ_UID     else _skip(),
        get_shiyu_defense(client)  if ZZZ_UID     else _skip(),
        get_deadly_assault(client) if ZZZ_UID     else _skip(),
        hsr_notes(client)          if HSR_UID     else _skip(),
    )


async def collect_one_time_data(client):
    return await asyncio.gather(
        genshin_abyss(client)               if GENSHIN_UID else _skip(),
        genshin_imaginarium_theater(client) if GENSHIN_UID else _skip(),
        stygian_onslaught(client)           if GENSHIN_UID else _skip(),
        hsr_anomaly_arbitration(client)     if HSR_UID     else _skip(),
        hsr_apocalyptic_shadow(client)      if HSR_UID     else _skip(),
        hsr_pure_fiction(client)            if HSR_UID     else _skip(),
        hsr_challenge(client)               if HSR_UID     else _skip(),
    )
