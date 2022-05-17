from datetime import datetime

from dateutil import parser
from db.contract_volumes_repo import ContractVolumesRepo
from ekp_sdk.services import CoingeckoService

class SingleCollectionsService:
    def __init__(
        self,
        contract_volumes_repo: ContractVolumesRepo,
        coingecko_service: CoingeckoService,
    ):
        self.contract_volumes_repo = contract_volumes_repo
        self.coingecko_service = coingecko_service

    async def get_chart_documents(self, currency, address):
        rate = await self.coingecko_service.get_latest_price('usd-coin', currency["id"])

        records = self.contract_volumes_repo.find_all_by_address(address)
        

        documents = list(map(lambda record: self.map_chart_document(record, rate), records))

        return documents

    def map_chart_document(self, record, rate):
        return {
            "timestamp": record["date_timestamp"],
            "timestampMs": record["date_timestamp"] * 1000,
            "address": record["address"],
            "name": record["name"],
            "volume": record["volume"],
            "volumeFiat": record["volume_usd"] * rate
        }
        
