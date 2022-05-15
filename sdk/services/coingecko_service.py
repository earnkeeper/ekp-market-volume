import json

import requests


class CoingeckoService:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"

    def get_coin_id_map(self, platform_id):
        url = f"{self.base_url}/coins/list?include_platform=true"

        print(f"🐛 {url}")

        response = json.loads(requests.get(url).text)

        map = {}

        for coin in response:
            if (platform_id not in coin["platforms"]):
                continue

            map[coin["platforms"][platform_id]] = coin["id"]

        return map

    def get_historic_price(self, coin_id, date_str):
        url = f"{self.base_url}/coins/{coin_id}/history?date={date_str}"

        print(f"🐛 {url}")

        response = json.loads(requests.get(url).text)

        return response['market_data']['current_price']
