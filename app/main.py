import asyncio

from decouple import config

from db.contract_volumes_repo import ContractVolumesRepo
from db.pg_db import PgDb
from db.tofu_buys_repo import TofuBuysRepo
from db.transactions_repo import TransactionsRepo
from sdk.coingecko_service import CoingeckoService
from sdk.etherscan_service import EtherscanService
from sdk.web3_service import Web3Service
from services.sync_transactions import sync_transactions
from services.transactions_decoder import TransactionsDecoder

if __name__ == '__main__':
    etherscan_service = EtherscanService(
        config('ETHERSCAN_API_KEY'), 
        config('ETHERSCAN_BASE_URL')
    )
    web3_service = Web3Service(config("WEB3_HTTP_PROVIDER"))
    coingecko_service = CoingeckoService()
    
    pg_db = PgDb()
    transactions_repo = TransactionsRepo(pg_db)
    tofu_buys_repo = TofuBuysRepo(pg_db)
    contract_volumes_repo = ContractVolumesRepo(pg_db)

    loop = asyncio.get_event_loop()

    transaction_decoder = TransactionsDecoder(
        coingecko_service,
        web3_service,
        transactions_repo,
        tofu_buys_repo,
        contract_volumes_repo        
    )
    
    transaction_decoder.decode_for_contract('0x449d05c544601631785a7c062dcdff530330317e')

    # Pegaxy Market
    loop.run_until_complete(
        sync_transactions(
            '0x449d05c544601631785a7c062dcdff530330317e',
            transactions_repo,
            config("MAX_TRANS_TO_FETCH", default=0, cast=int)
        )
    )
