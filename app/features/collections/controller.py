from app.features.collections.page import page
from app.features.collections.service import CollectionsService
from ekp_sdk.services import ClientService
from ekp_sdk.util import client_currency, client_path

TABLE_COLLECTION_NAME = "collection_volumes"
CHART_COLLECTION_NAME = "volume_chart"


class CollectionsController:
    def __init__(
        self,
        client_service: ClientService,
        collections_service: CollectionsService
    ):
        self.client_service = client_service
        self.collections_service = collections_service
        self.path = 'collections'

    async def on_connect(self, sid):
        await self.client_service.emit_menu(
            sid,
            'bar-chart',
            'Market Volumes',
            self.path
        )
        await self.client_service.emit_page(
            sid,
            self.path,
            page(TABLE_COLLECTION_NAME, CHART_COLLECTION_NAME)
        )

    async def on_client_state_changed(self, sid, event):
        path = client_path(event)
        if not path or not path.startswith("collections"):
            return

        await self.client_service.emit_busy(sid, TABLE_COLLECTION_NAME)
        await self.client_service.emit_busy(sid, CHART_COLLECTION_NAME)

        currency = client_currency(event)

        chart_documents = await self.collections_service.get_chart_documents(currency)
        
        await self.client_service.emit_documents(
            sid,
            CHART_COLLECTION_NAME,
            chart_documents
        )
        
        await self.client_service.emit_done(sid, CHART_COLLECTION_NAME)

        table_documents = await self.collections_service.get_table_documents(currency)
        
        await self.client_service.emit_documents(
            sid,
            TABLE_COLLECTION_NAME,
            table_documents
        )

        await self.client_service.emit_done(sid, TABLE_COLLECTION_NAME)
