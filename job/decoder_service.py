
from db.contract_volumes_repo import ContractVolumesRepo
from db.tofu_buys_repo import TofuBuysRepo
from db.transactions_repo import TransactionsRepo
from sdk.services.coingecko_service import CoingeckoService
from sdk.services.etherscan_service import EtherscanService
from sdk.services.web3_service import Web3Service
import math

class DecoderService:
    def __init__(
        self,
        coingecko_service: CoingeckoService,
        contract_volumes_repo: ContractVolumesRepo,
        etherscan_service: EtherscanService,
        tofu_buys_repo: TofuBuysRepo,
        transactions_repo: TransactionsRepo,
        web3_service: Web3Service,
    ):
        self.coingecko_service = coingecko_service
        self.contract_volumes_repo = contract_volumes_repo
        self.etherscan_service = etherscan_service
        self.tofu_buys_repo = tofu_buys_repo
        self.transactions_repo = transactions_repo
        self.web3_service = web3_service

    def decode_transactions(self, query_address):
        print("✨ Decoding transactions")

        abi = self.etherscan_service.get_abi(query_address)

        coin_id_map = self.coingecko_service.get_coin_id_map(
            "binance-smart-chain"
        )

        rates = {
            "usd": {
                "14-05-2022": 1.0
            }
        }

        currency_decimals = {}

        page_size = 10000
        start_timestamp = 0

        latest = self.tofu_buys_repo.find_latest()

        contract_volumes = self.contract_volumes_repo.find_all()

        if latest is not None:
            start_timestamp = latest["timestamp_unix"]

        while (True):
            next = self.transactions_repo.find_next_by_source(
                query_address,
                '0xba847759',
                start_timestamp,
                page_size
            )

            if (len(next) == 0):
                break

            print(f"🐛 Decoding {len(next)} transactions..")

            models = []

            for next_tran in next:
                
                next_timestamp = next_tran["timestamp_unix"]
                
                if next_timestamp > start_timestamp:
                    start_timestamp = next_timestamp
                    
                model = self.decode_transaction(
                    next_tran,
                    abi,
                    coin_id_map,
                    rates,
                    currency_decimals,
                    contract_volumes
                )
                models.append(model)

            self.tofu_buys_repo.save(models)
            self.contract_volumes_repo.save(contract_volumes)

    def decode_transaction(
        self,
        next_tran,
        abi,
        coin_id_map,
        rates,
        currency_decimals,
        contract_volumes
    ):
        decoded = self.web3_service.decode_input(abi, next_tran["input"])
        currency = decoded["detail"][7]

        coin_id = None

        if currency == "0x0000000000000000000000000000000000000000":
            currency = "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"
            coin_id = "wbnb"
        else:
            if currency in coin_id_map:
                coin_id = coin_id_map[currency]

        date_str = next_tran["timestamp"].strftime("%d-%m-%Y")

        if (coin_id not in rates):
            rates[coin_id] = {}

        if (date_str not in rates[coin_id]):
            rates[coin_id][date_str] = self.coingecko_service.get_historic_price(
                coin_id, date_str)["usd"]

        if currency not in currency_decimals:
            currency_decimals[currency] = self.web3_service.get_currency_decimals(
                currency)

        rate = rates[coin_id][date_str]
        decimals = currency_decimals[currency]

        value = decoded["detail"][8]
        value = int(value) / math.pow(10, decimals)
        value_usd = value * rate

        contract_volume = next(
            (item for item in contract_volumes if item["date_str"] == date_str and item["address"] == next_tran["to"]), None)

        if contract_volume is None:

            contract_volume = {
                "date_str": date_str,
                "address": next_tran["to"],
                "name": self.etherscan_service.get_contract_name(next_tran["to"]),
                "volume": 0,
                "volume_usd": 0
            }

            contract_volumes.append(contract_volume)

        contract_volume["volume"] = contract_volume["volume"] + 1
        contract_volume["volume_usd"] = contract_volume["volume_usd"] + value_usd

        return {
            'hash': next_tran["hash"],
            'block_number': next_tran["block_number"],
            'gas_price': next_tran["gas_price"],
            'gas_used': next_tran["gas_used"],
            'nft_contract_address': next_tran["to"],
            'value': value,
            'currency': currency,
            'value_usd': value_usd,
            'timestamp': next_tran["timestamp"],
            'timestamp_unix': next_tran["timestamp_unix"],
        }
