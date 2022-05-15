from web3.auto import w3, Web3
from decouple import config

class Web3Service:
    def __init__(self, provider):
        if provider is None:
            self.w3 = w3
        else:
            self.w3 = Web3(Web3.HTTPProvider(provider))

    def decode_input(self, abi, input):

        contract = self.w3.eth.contract(abi=abi)
        func_obj, func_params = contract.decode_function_input(input)

        return func_params

    def get_currency_decimals(self, address):
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

        return contract.functions.decimals().call()
