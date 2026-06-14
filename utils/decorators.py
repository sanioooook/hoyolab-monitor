import asyncio
import functools
import json
import genshin
from twocaptcha import TwoCaptcha, ApiException, NetworkException, SolverExceptions, ValidationException, TimeoutException
from config import TWOCAPTCHA_API_KEY


def handle_geetest(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            # Attempt to execute the wrapped function
            return await func(*args, **kwargs)

        except genshin.GeetestError as e:
            print(f"[Geetest] Captcha triggered in {func.__name__}: {e}")
            solver = TwoCaptcha(TWOCAPTCHA_API_KEY)

            # Extract client object (can be passed explicitly or as first argument)
            local_client = None
            for arg in args:
                if isinstance(arg, genshin.Client):
                    local_client = arg
                    break
            if local_client is None:
                print("[Geetest] Could not find genshin.Client in arguments.")
                return None

            for attempt in range(1, 4):
                try:
                    # Step 1: Create MMT challenge
                    mmt = await local_client.create_mmt()

                    # Step 2: Prepare verification URL
                    url = genshin.client.routes.CREATE_MMT_URL.get_url(genshin.types.Region.OVERSEAS)
                    url = url.update_query(app_key=genshin.constants.GEETEST_RECORD_KEYS[local_client.default_game])

                    # Step 3: Solve via 2Captcha
                    solved = solver.geetest(gt=mmt.gt, challenge=mmt.challenge, url=url)
                    solved_code = json.loads(solved["code"])

                    # Step 4: Send verification result to HoYoLab
                    mmt_result = genshin.models.MMTResult(
                        geetest_challenge=solved_code["geetest_challenge"],
                        geetest_validate=solved_code["geetest_validate"],
                        geetest_seccode=solved_code["geetest_seccode"]
                    )
                    await local_client.verify_mmt(mmt_result)

                    print(f"[Geetest] Solved successfully on attempt {attempt}, retrying {func.__name__}...")
                    return await func(*args, **kwargs)

                except (ValidationException, NetworkException, ApiException, TimeoutException, SolverExceptions) as ex:
                    print(f"[Geetest] Attempt {attempt} failed: {ex}")
                    await asyncio.sleep(2 ** attempt)  # exponential backoff
                except Exception as ex:
                    print(f"[Geetest] Unexpected error during solving: {ex}")
                    break

            print(f"[Geetest] Failed to solve captcha after 3 attempts for {func.__name__}.")
            return None

        except Exception as ex:
            print(f"[Geetest] General error in {func.__name__}: {ex}")
            return None

    return wrapper
