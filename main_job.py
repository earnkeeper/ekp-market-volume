import asyncio

from decouple import config
from ekp_sdk import BaseContainer

from db.contract_volumes_repo import ContractVolumesRepo
from db.tofu_buys_repo import TofuBuysRepo
from db.transactions_repo import TransactionsRepo
from job.decoder_service import DecoderService
from job.sync_service import SyncService

MARKET_CONTRACT = '0x449d05c544601631785a7c062dcdff530330317e'


class AppContainer(BaseContainer):
    def __init__(self):
        MAX_TRANS_TO_FETCH = config("MAX_TRANS_TO_FETCH", cast=int, default=0)

        super().__init__()

        self.contract_volumes_repo = ContractVolumesRepo(
            pg_client=self.pg_client,
        )

        self.tofu_buys_repo = TofuBuysRepo(
            pg_client=self.pg_client,
        )

        self.transactions_repo = TransactionsRepo(
            pg_client=self.pg_client,
        )

        self.sync_service = SyncService(
            etherscan_service=self.etherscan_service,
            max_trans_to_fetch=MAX_TRANS_TO_FETCH,
            transactions_repo=self.transactions_repo,
        )

        self.decoder_service = DecoderService(
            cache_service=self.cache_service,
            coingecko_service=self.coingecko_service,
            contract_volumes_repo=self.contract_volumes_repo,
            etherscan_service=self.etherscan_service,
            tofu_buys_repo=self.tofu_buys_repo,
            transactions_repo=self.transactions_repo,
            web3_service=self.web3_service,
        )


if __name__ == '__main__':
    container = AppContainer()

    print("🚀 Application Start")

    loop = asyncio.get_event_loop()

    loop.run_until_complete(
        container.sync_service.sync_transactions(MARKET_CONTRACT)
    )
    loop.run_until_complete(
        container.decoder_service.decode_transactions(MARKET_CONTRACT)
    )
