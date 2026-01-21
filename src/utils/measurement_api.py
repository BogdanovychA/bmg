# -*- coding: utf-8 -*-

import httpx

from utils.secret import GA_SECRET_KEY

GA_ID = "G-GHW1HZTWBV"

async_client = httpx.AsyncClient()


async def log_event(client_id: str, platform: str, event_name: str, page_path: str):

    url = f"https://www.google-analytics.com/mp/collect?measurement_id={GA_ID}&api_secret={GA_SECRET_KEY}"
    # url = f"https://www.google-analytics.com/debug/mp/collect?measurement_id={GA_ID}&api_secret={GA_SECRET_KEY}"

    payload = {
        "client_id": client_id,
        "events": [
            {
                "name": event_name,
                "params": {
                    "page_path": page_path,
                    "platform": platform,
                },
            }
        ],
    }

    try:
        response = await async_client.post(url, json=payload, timeout=5.0)
        # Для DEBUG-урла ми очікуємо 200 і дивимося всередину JSON
        if "/debug/" in url:
            print("Debug Validation Result:")
            print(response.json())  # <--- Ось тут буде відповідь від Google
        else:
            # Для реального збору даних очікуємо 204
            if response.status_code == 204:
                # print("Event sent successfully!")
                pass
            else:
                print(f"GA Error: {response.status_code}")
    except Exception as e:
        print(f"Could not send analytics: {e}")
