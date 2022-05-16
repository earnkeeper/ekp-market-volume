from datetime import datetime

from dateutil import parser
from db.contract_volumes_repo import ContractVolumesRepo
from ekp_sdk.services import CoingeckoService

class CollectionsService:
    def __init__(
        self,
        contract_volumes_repo: ContractVolumesRepo,
        coingecko_service: CoingeckoService,
    ):
        self.contract_volumes_repo = contract_volumes_repo
        self.coingecko_service = coingecko_service

    async def get_chart_documents(self, currency):
        records = self.contract_volumes_repo.find_all()
        
        rate = await self.coingecko_service.get_latest_price('usd-coin', currency["id"])

        grouped_by_date_str = {}

        for record in records:
            date_str = record["date_str"]
            date_timestamp = record["date_timestamp"]
            updated = record["updated"]

            if date_str not in grouped_by_date_str:
                grouped_by_date_str[date_str] = {
                    "id": date_str,
                    "fiatSymbol": currency["symbol"],
                    "timestamp": date_timestamp,
                    "timestamp_ms": date_timestamp * 1000,
                    "updated": record["updated"],
                    "volume": 0,
                    "volume_fiat": 0,
                }

            group = grouped_by_date_str[date_str]

            if updated > group["updated"]:
                group["updated"] = updated
            group["volume"] = group["volume"] + record["volume"]
            group["volume_fiat"] = group["volume_fiat"] + \
                record["volume_usd"] * rate

        documents = list(grouped_by_date_str.values())

        return documents

    async def get_table_documents(self, currency):
        records = self.contract_volumes_repo.find_all()
        
        rate = await self.coingecko_service.get_latest_price('usd-coin', currency["id"])
        
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
                group["volume24hUsd"] = group["volume24hUsd"] + \
                    record["volume_usd"] * rate
            
            if ago < (86400 * 7):
                group["volume7d"] = group["volume7d"] + record["volume"]
                group["volume7dUsd"] = group["volume7dUsd"] + \
                    record["volume_usd"] * rate
                group["chart7d"].append({
                    "timestamp": date_timestamp,
                    "timestamp_ms": date_timestamp * 1000,
                    "volume": record["volume"],
                    "volume_usd": record["volume_usd"] * rate,
                })

        documents = list(grouped_by_address.values())

        return documents
