import json
from decouple import config
import aiohttp
from sdk.retry import default_retry_policy
from aioretry import retry
from datetime import datetime

@retry(default_retry_policy)
async def get_transactions(url, session):
    print(url)
    
    response = await session.get(url=url)
    
    if (response.status != 200):
        raise Exception(f"Response code: {response.status}")
            
    text = await response.read()
    data = json.loads(text.decode())
    trans = data["result"]
    
    if (trans is None):
        print(text)
        raise Exception("Received None data from url")

    return trans


async def sync_transactions(query_address, transactions_repo, max_trans_to_fetch=0):
    start_block = 0
    page_size = 5000

    latest = transactions_repo.find_latest()

    if latest is not None:
        start_block = latest["block_number"]
        
    async with aiohttp.ClientSession() as session:
        while (True):
            url = f'https://api.bscscan.com/api?module=account&action=txlist&address={query_address}&startblock={start_block}&page=1&offset={page_size}&sort=asc&apiKey={BSCSCAN_API_KEY}'
            
            trans = await get_transactions(url, session)
            
            if (len(trans) == 0):   
                break

            print(f"Retrieved {len(trans)} from the api, saving to db...")

            models = []
            
            for tran in trans:
                block_number = int(tran["blockNumber"])

                if (block_number > start_block):
                    start_block = block_number
                    
                model = {
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
                
                models.append(model)

            transactions_repo.save(models)

            if (len(trans) < page_size or max_trans_to_fetch > 0 and len(trans) > max_trans_to_fetch):
                break