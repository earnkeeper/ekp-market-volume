from services.transaction_decoder import TransactionDecoder


class TransactionsDecoder:
    def __init__(
        self,
        coingecko_service,
        contract_volumes_repo,
        etherscan_service,
        tofu_buys_repo,
        transactions_repo,
        web3_service,
    ):
        self.coingecko_service = coingecko_service,
        self.web3_service = web3_service,
        self.transactions_repo = transactions_repo,
        self.tofu_buys_repo = tofu_buys_repo,
        self.contract_volumes_repo = contract_volumes_repo
        self.etherscan_service = etherscan_service
        self.transaction_decoder = TransactionDecoder(
            coingecko_service,
            etherscan_service,
            web3_service,
        )

    def decode_for_contract(self, query_address):
        abi = self.web3_service.get_abi(query_address)

        coin_id_map = self.coingecko_service.fetch_coin_id_map(
            "binance-smart-chain")

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

            models = []

            for next_tran in next:
                model = self.transaction_decoder.decode(
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
