import requests
import json

BASE_URL="https://api.coingecko.com/api/v3"
class CoingeckoService:
    def fetch_coin_id_map(self, platform_id):
        url = f"{BASE_URL}/coins/list?include_platform=true";
        
        print(url)
        response = json.loads(requests.get(url).text)
        
        map = {}
        
        for coin in response:
            if (platform_id not in coin["platforms"]):
                continue;
            
            map[coin["platforms"][platform_id]] = coin["id"]
            
        return map
    
    def fetch_historic_price(self, coin_id, date_str):
        url = f"{BASE_URL}/coins/{coin_id}/history?date={date_str}"
        
        print(url)
        response = json.loads(requests.get(url).text)
        
        return response['market_data']['current_price']