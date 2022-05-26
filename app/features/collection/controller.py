from app.features.collection.service import SingleCollectionsService
from app.features.collection.page import page
from ekp_sdk.services import ClientService
from ekp_sdk.util import client_currency, client_path

TABLE_COLLECTION_NAME = "single_collection_volumes"
CHART_COLLECTION_NAME = "single_volume_chart"


class SingleCollectionController:
    def __init__(
        self,
        client_service: ClientService,
        collection_service: SingleCollectionsService
    ):
        self.client_service = client_service
        self.service = collection_service
        self.path = 'collection/:collectionAddress'

    async def on_connect(self, sid):
        await self.client_service.emit_page(
            sid,
            self.path,
            page(TABLE_COLLECTION_NAME, CHART_COLLECTION_NAME)
        )

    async def on_client_state_changed(self, sid, event):
        path = client_path(event)
        if not path or not path.startswith("collection/"):
            return
        
        await self.client_service.emit_busy(sid, CHART_COLLECTION_NAME)

        currency = client_currency(event)
        address = path.replace("collection/", "")
        chart_documents = await self.service.get_chart_documents(currency, address)
        
        await self.client_service.emit_documents(
            sid,
            CHART_COLLECTION_NAME,
            chart_documents
        )
        
        await self.client_service.emit_done(sid, CHART_COLLECTION_NAME)

