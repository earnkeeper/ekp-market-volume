import json
import time

import aiohttp
from aioretry import retry
from sdk.services.retry import default_retry_policy


class RestClient:

    @retry(default_retry_policy)
    async def get(self, url, fn=lambda data, text: data):
        async with aiohttp.ClientSession() as session:
            print(f"🐛 {url}")
            start = time.perf_counter()
            response = await session.get(url=url)

            if (response.status != 200):
                raise Exception(f"Response code: {response.status}")

            text = await response.read()
            data = json.loads(text.decode())

            print(f"⏱  [{url}] {time.perf_counter() - start:0.3f}s")
            
            return fn(data, text)
