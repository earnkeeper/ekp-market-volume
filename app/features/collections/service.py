from db.contract_volumes_repo import ContractVolumesRepo
from dateutil import parser
from datetime import datetime

class CollectionsService:
    def __init__(
        self,
        contract_volumes_repo: ContractVolumesRepo
    ):
        self.contract_volumes_repo = contract_volumes_repo

    def get_documents(self, currency):
        records = self.contract_volumes_repo.find_all()
        
        grouped_by_address = {}
        
        for record in records:
            address = record["address"]
            date_timestamp = record["date_timestamp"]
            updated = record["updated"]
            
            if address not in grouped_by_address:
                grouped_by_address[address] = {
                    "collectionAddress": address,
                    "collectionName": record["name"],
                    "blockchain": "BSC",
                    "volume24h": 0,
                    "volume7d": 0,
                    "volume24hUsd": 0,
                    "volume7dUsd": 0,
                    "latestTimestamp": 0,
                    "updated": record["updated"],
                    "fiatSymbol": currency["symbol"],
                    "chart7d": []
                }
                
            group = grouped_by_address[address]
            
            if date_timestamp > group["latestTimestamp"]:
                group["latestTimestamp"] = date_timestamp
                
            if updated > group["updated"]:
                group["updated"] = updated
                

        for record in records:
            address = record["address"]
            date_timestamp = int(parser.parse(record["date_str"]).timestamp())
            group = grouped_by_address[address]
            ago = group["latestTimestamp"] - date_timestamp
            if ago < 86400:
                group["volume24h"] = group["volume24h"] + record["volume"]
                group["volume24hUsd"] = group["volume24hUsd"] + record["volume_usd"]
            if ago < (86400 * 7):
                group["volume7d"] = group["volume7d"] + record["volume"]
                group["volume7dUsd"] = group["volume7dUsd"] + record["volume_usd"]
                group["chart7d"].append({
                    "timestamp": date_timestamp,
                    "timestamp_ms": date_timestamp * 1000,
                    "volume": record["volume"],
                    "volume_usd": record["volume_usd"],
                })
        
        
        documents = list(grouped_by_address.values())
        
        return documents
