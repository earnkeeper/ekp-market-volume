import requests
import json

from sdk.retry import default_retry_policy
from aioretry import retry

class EtherscanService:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url

    def get_contract_name(self, address):
        url = f"{self.base_url}?module=contract&action=getsourcecode&address={address}&apikey={self.api_key}"
        results = json.loads(requests.get(url).text)["result"]
        return results[0]["ContractName"]

    def get_abi(self, address):
        abi_endpoint = f"{self.base_url}?module=contract&action=getabi&address={address}&apikey={self.api_key}"
        return json.loads(requests.get(abi_endpoint).text)["result"]
    
    @retry(default_retry_policy)
    async def get_transactions(self, address, start_block, offset):
        async with aiohttp.ClientSession() as session:

            url = f'{self.base_url}?module=account&action=txlist&address={address}&startblock={start_block}&page=1&offset={offset}&sort=asc&apiKey={self.api_key}'
                
            response = await session.get(url=url)
        
            if (response.status != 200):
                raise Exception(f"Response code: {response.status}")
                    
            text = await response.read()
            data = json.loads(text.decode())
            trans = data["result"]
            
            if (trans is None):
                print(text)
                raise Exception("Received None data from url")

            return trans


