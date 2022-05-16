import time
from decouple import config
from web3.auto import Web3, w3


class Web3Service:
    def __init__(self, provider_url):
        if provider_url is None:
            self.w3 = w3
        else:
            self.w3 = Web3(Web3.HTTPProvider(provider_url))

    def decode_input(self, abi, input):

        contract = self.w3.eth.contract(abi=abi)
        func_obj, func_params = contract.decode_function_input(input)

        return func_params

    async def get_currency_decimals(self, address):
        start = time.perf_counter()

        address = Web3.toChecksumAddress(address)

        decimals_abi = [
            {
                "constant": True,
                "inputs": [],
                "name": "decimals",
                "outputs": [{"name": "", "type": "uint8"}],
                "payable": False,
                "stateMutability": "view",
                "type": "function"
            }
        ]

        contract = self.w3.eth.contract(address=address, abi=decimals_abi)

        print(f'🐛 contract("{address}").decimals.call()')

        result = contract.functions.decimals().call()

        print(
            f"⏱  [web3_service.get_currency_decimals] {time.perf_counter() - start:0.3f}s")

        return result

    async def get_token_name(self, address):
        start = time.perf_counter()

        try:
            address = Web3.toChecksumAddress(address)

            name_abi = [
                {
                    "inputs": [],
                    "name": "name",
                    "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                    "stateMutability": "view",
                    "type": "function"
                }
            ]

            contract = self.w3.eth.contract(address=address, abi=name_abi)

            print(f'🐛 contract("{address}").name.call()')

            result = contract.functions.name().call()
            
            print(f"⏱  [web3_service.get_token_name] {time.perf_counter() - start:0.3f}s")
            
            return result
        except:
            print(f"🚨 [web3_service.get_token_name] {time.perf_counter() - start:0.3f}s")
            return None


