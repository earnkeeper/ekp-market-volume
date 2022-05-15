
import math

from db.contract_volumes_repo import ContractVolumesRepo
from db.tofu_buys_repo import TofuBuysRepo
from db.transactions_repo import TransactionsRepo
from sdk.services.cache_service import CacheService
from sdk.services.coingecko_service import CoingeckoService
from sdk.services.etherscan_service import EtherscanService
from sdk.services.web3_service import Web3Service


class DecoderService:
    def __init__(
        self,
        cache_service: CacheService,
        coingecko_service: CoingeckoService,
        contract_volumes_repo: ContractVolumesRepo,
        etherscan_service: EtherscanService,
        tofu_buys_repo: TofuBuysRepo,
        transactions_repo: TransactionsRepo,
        web3_service: Web3Service,
    ):
        self.cache_service = cache_service
        self.coingecko_service = coingecko_service
        self.contract_volumes_repo = contract_volumes_repo
        self.etherscan_service = etherscan_service
        self.tofu_buys_repo = tofu_buys_repo
        self.transactions_repo = transactions_repo
        self.web3_service = web3_service

    async def decode_transactions(self, query_address):
        self.coin_id_map = await self.cache_service.wrap(
            "coin_id_map",
            ex=86400,
            fn=lambda: self.coingecko_service.get_coin_id_map(
                "binance-smart-chain"
            )
        )

        print("✨ Decoding transactions")

        query_abi = await self.etherscan_service.get_abi(query_address)

        page_size = 10000
        start_timestamp = 0

        latest = self.tofu_buys_repo.find_latest()

        contract_volumes = self.contract_volumes_repo.find_all()

        def clone_contract_volume(model):
            return {
                'date_str': model["date_str"],
                'address': model["address"],
                'name': model["name"],
                'volume': model["volume"],
                'volume_usd': model["volume_usd"],
            }

        contract_volumes = list(map(clone_contract_volume, contract_volumes))

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

            print(f"✨ Decoding {len(next)} transactions..")

            models = []

            for next_tran in next:

                next_timestamp = next_tran["timestamp_unix"]

                if next_timestamp > start_timestamp:
                    start_timestamp = next_timestamp

                model = await self.decode_transaction(
                    next_tran,
                    query_abi,
                    contract_volumes
                )
                models.append(model)

            self.tofu_buys_repo.save(models)
            self.contract_volumes_repo.save(contract_volumes)

    async def decode_transaction(
        self,
        next_tran,
        query_abi,
        contract_volumes
    ):
        decoded = self.web3_service.decode_input(query_abi, next_tran["input"])
        currency = decoded["detail"][7]
        value = decoded["detail"][8]
        contract_address = decoded["detail"][11][0][0]

        coin_id = None

        if currency == "0x0000000000000000000000000000000000000000":
            currency = "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"
            coin_id = "wbnb"
        else:
            if currency in self.coin_id_map:
                coin_id = self.coin_id_map[currency]

        date_str = next_tran["timestamp"].strftime("%d-%m-%Y")

        rates_key = f"coin_price_{coin_id}_{date_str}"

        rate = await self.cache_service.wrap(
            key=rates_key,
            fn=lambda: self.coingecko_service.get_historic_price(
                coin_id, date_str, "usd"
            )
        )

        decimals_key = f"decimals_{currency}"

        decimals = await self.cache_service.wrap(
            key=decimals_key,
            fn=lambda: self.web3_service.get_currency_decimals(currency)
        )

        value = int(value) / math.pow(10, decimals)
        value_usd = value * rate

        contract_volume = next(
            (item for item in contract_volumes if item["date_str"] == date_str and item["address"] == next_tran["to"]), None)

        if contract_volume is None:

            contract_name_key = f"contract_name_{contract_address}"
            contract_name = await self.cache_service.wrap(
                key=contract_name_key,
                fn=lambda: self.etherscan_service.get_contract_name(
                    contract_address)
            )
            contract_volume = {
                "date_str": date_str,
                "address": contract_address,
                "name": contract_name,
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
            'nft_contract_address': contract_address,
            'value': value,
            'currency': currency,
            'value_usd': value_usd,
            'timestamp': next_tran["timestamp"],
            'timestamp_unix': next_tran["timestamp_unix"],
        }
