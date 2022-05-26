import copy

from db.contract_volumes_repo import ContractVolumesRepo
from ekp_sdk.services import CoingeckoService
from app.utils.strings import title_to_kebab

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
        rate = await self.coingecko_service.get_latest_price('usd-coin', currency["id"])

        records = self.contract_volumes_repo.find_all()

        if not len(records):
            return []
        
        latest_date_timestamp = records[len(records) - 1]["date_timestamp"]

        chart7d_template = {}

        for i in range(7):
            chart_timestamp = latest_date_timestamp - 86400 * (6-i)
            chart7d_template[chart_timestamp] = {
                "timestamp": chart_timestamp,
                "timestamp_ms": chart_timestamp * 1000,
                "volume": 0,
                "volume_usd": 0,
            }

        grouped_by_address = {}

        for record in records:
            address = record["address"]
            date_timestamp = record["date_timestamp"]
            updated = record["updated"]
            ago = latest_date_timestamp - date_timestamp
            volume = record["volume"]
            volume_usd = record["volume_usd"]

            if address not in grouped_by_address:
                grouped_by_address[address] = {
                    "collectionAddress": address,
                    "collectionName": record["name"],
                    "collectionSlug": title_to_kebab(record["name"]),
                    "blockchain": "BSC",
                    "volume24h": 0,
                    "volume7d": 0,
                    "volume24hUsd": 0,
                    "volume7dUsd": 0,
                    "updated": record["updated"],
                    "fiatSymbol": currency["symbol"],
                    "chart7d": copy.deepcopy(chart7d_template)
                }

            group = grouped_by_address[address]

            if updated > group["updated"]:
                group["updated"] = updated

            if ago == 0:
                group["volume24h"] = group["volume24h"] + volume
                group["volume24hUsd"] = group["volume24hUsd"] + \
                    volume_usd * rate

            if ago < (86400 * 7):
                group["volume7d"] = group["volume7d"] + volume
                group["volume7dUsd"] = group["volume7dUsd"] + \
                    record["volume_usd"] * rate

            if date_timestamp in group["chart7d"]:
                group["chart7d"][date_timestamp]["volume"] = volume
                group["chart7d"][date_timestamp]["volume_usd"] = volume_usd * rate

        documents = list(
            filter(lambda x: x["volume7d"], grouped_by_address.values())
        )

        return documents
