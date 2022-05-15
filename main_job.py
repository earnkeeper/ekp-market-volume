import asyncio

from decouple import config
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

from db.contract_volumes_repo import ContractVolumesRepo
from db.tofu_buys_repo import TofuBuysRepo
from db.transactions_repo import TransactionsRepo
from job.decoder_service import DecoderService
from job.sync_service import SyncService
from sdk.db.pg_client import PgClient
from sdk.services.coingecko_service import CoingeckoService
from sdk.services.etherscan_service import EtherscanService
from sdk.services.web3_service import Web3Service

MARKET_CONTRACT = '0x449d05c544601631785a7c062dcdff530330317e'


class Container(containers.DeclarativeContainer):

    POSTGRES_URI = config("POSTGRES_URI")
    ETHERSCAN_API_KEY = config("ETHERSCAN_API_KEY")
    ETHERSCAN_BASE_URL = config("ETHERSCAN_BASE_URL")
    WEB3_PROVIDER_URL = config("WEB3_PROVIDER_URL")
    MAX_TRANS_TO_FETCH = config("MAX_TRANS_TO_FETCH", cast=int, default=0)

    coingecko_service = providers.Singleton(
        CoingeckoService,
    )

    etherscan_service = providers.Singleton(
        EtherscanService,
        api_key=ETHERSCAN_API_KEY,
        base_url=ETHERSCAN_BASE_URL,
    )

    pg_client = providers.Singleton(
        PgClient,
        uri=POSTGRES_URI,
    )

    web3_service = providers.Singleton(
        Web3Service,
        provider_url=WEB3_PROVIDER_URL,
    )

    contract_volumes_repo = providers.Singleton(
        ContractVolumesRepo,
        pg_client=pg_client,
    )

    tofu_buys_repo = providers.Singleton(
        TofuBuysRepo,
        pg_client=pg_client,
    )

    transactions_repo = providers.Singleton(
        TransactionsRepo,
        pg_client=pg_client,
    )

    sync_service = providers.Singleton(
        SyncService,
        etherscan_service=etherscan_service,
        max_trans_to_fetch=MAX_TRANS_TO_FETCH,
        transactions_repo=transactions_repo,
    )

    decoder_service = providers.Singleton(
        DecoderService,
        coingecko_service=coingecko_service,
        contract_volumes_repo=contract_volumes_repo,
        etherscan_service=etherscan_service,
        tofu_buys_repo=tofu_buys_repo,
        transactions_repo=transactions_repo,
        web3_service=web3_service,

    )


@inject
def main(
    sync_service: SyncService = Provide[Container.sync_service],
    decoder_service: DecoderService = Provide[Container.decoder_service]
):
    print("🚀 Application Start")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        sync_service.sync_transactions(MARKET_CONTRACT)
    )
    loop.run_until_complete(
        decoder_service.decode_transactions(MARKET_CONTRACT)
    )


if __name__ == '__main__':
    container = Container()
    container.wire(modules=[__name__])

    main()
