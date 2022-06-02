from app.features.embeds.embed_tile import embed_tile
from db.contract_volumes_repo import ContractVolumesRepo
from ekp_sdk.services import CoingeckoService
from datetime import datetime
from pprint import pprint


class EmbedsService:

    def __init__(
        self,
        contract_volumes_repo: ContractVolumesRepo,
        coingecko_service: CoingeckoService
    ):
        self.contract_volumes_repo = contract_volumes_repo
        self.coingecko_service = coingecko_service

    async def get_embeds(self, currency):

        embeds = []

        timestamp_30d_ago = datetime.now().timestamp() - (60 * 1440 * 30)
        timestamp_1d_ago = datetime.now().timestamp() - (60 * 1440 * 2)

        # TODO
        top_10_addresses = self.contract_volumes_repo.group_by_address_and_name(
            timestamp_1d_ago,
            10
        )

        rate = await self.coingecko_service.get_latest_price("usd-coin", currency["id"])

        for i in range(0, 10):
            address = top_10_addresses[i]['address']
            name = top_10_addresses[i]['name']
            sales24h = top_10_addresses[i]['volume']
            volume24h = top_10_addresses[i]['volume_usd']

            chart_30d = []

            records_30d = self.contract_volumes_repo.find_all_by_address(address, since=timestamp_30d_ago)

            for record in records_30d:
                chart_30d.append({
                    "timestamp_ms": record["date_timestamp"] * 1000,
                    "sales": record["volume"],
                    "volume": record["volume_usd"] * rate
                })

            data_document = {
                "address": address,
                "name": name,
                "rank": i + 1,
                "sales24h": sales24h,
                "volume24h": volume24h * rate,
                "fiatSymbol": currency["symbol"],
                "chart30d": chart_30d
            }

            embed = {
                "id": 'market_volume_1',
                "size": 'tile',
                "element": embed_tile(),
                "data": [data_document],
                "page": 'collections',
            }

            embeds.append(embed)

        return embeds
