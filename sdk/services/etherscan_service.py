from sdk.services.rest_client import RestClient


class EtherscanService:
    def __init__(
        self,
        api_key,
        base_url,
        rest_client: RestClient
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.rest_client = rest_client

    async def get_contract_name(self, address):
        url = f"{self.base_url}?module=contract&action=getsourcecode&address={address}&apikey={self.api_key}"

        result = await self.rest_client.get(url, lambda data, text: data["result"][0]["ContractName"])

        return result

    async def get_abi(self, address):
        url = f"{self.base_url}?module=contract&action=getabi&address={address}&apikey={self.api_key}"

        result = await self.rest_client.get(url, lambda data, text: data["result"])

        return result

    async def get_transactions(self, address, start_block, offset):

        url = f'{self.base_url}?module=account&action=txlist&address={address}&startblock={start_block}&page=1&offset={offset}&sort=asc&apiKey={self.api_key}'

        def fn(data, text):
            trans = data["result"]

            if (trans is None):
                print(f"🚨 {text}")
                raise Exception("Received None data from url")

            return trans

        result = await self.rest_client.get(url, fn)

        return result
