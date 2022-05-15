from datetime import datetime

from db.transactions_repo import TransactionsRepo
from sdk.services.etherscan_service import EtherscanService


class SyncService:
    def __init__(
        self,
        etherscan_service: EtherscanService,
        max_trans_to_fetch: int,
        transactions_repo: TransactionsRepo,
    ) -> None:
        self.etherscan_service = etherscan_service
        self.max_trans_to_fetch = max_trans_to_fetch
        self.transactions_repo = transactions_repo

    async def sync_transactions(self, query_address):
        print("✨ Syncing transactions")
        start_block = 0
        page_size = 5000

        if (self.max_trans_to_fetch > 0):
            page_size = self.max_trans_to_fetch

        latest = self.transactions_repo.find_latest()

        if latest is not None:
            start_block = latest["block_number"]

        while (True):
            trans = await self.etherscan_service.get_transactions(query_address, start_block, offset=page_size)

            if (len(trans) == 0):
                break

            print(f"👍 Retrieved {len(trans)} from the api, saving to db...")

            models = []

            for tran in trans:
                block_number = int(tran["blockNumber"])

                if (block_number > start_block):
                    start_block = block_number

                model = self.map_model(query_address, tran)

                models.append(model)

            self.transactions_repo.save(models)

            if (len(trans) < page_size or self.max_trans_to_fetch > 0 and len(trans) >= self.max_trans_to_fetch):
                break

    def map_model(self, query_address, tran):
        return {
            "hash": tran["hash"],
            "block_hash": tran["blockHash"],
            "block_number": tran["blockNumber"],
            "cumulative_gas_used": int(tran["cumulativeGasUsed"]),
            "from": tran["from"],
            "gas_price": int(tran["gasPrice"]),
            "gas_used": int(tran["gasUsed"]),
            "input": tran["input"],
            "is_error": tran["isError"] == "1",
            "query_address": query_address,
            "timestamp": datetime.fromtimestamp(int(tran["timeStamp"])),
            "timestamp_unix": int(tran["timeStamp"]),
            "to": tran["to"],
            "transaction_index": int(tran["transactionIndex"]),
        }
