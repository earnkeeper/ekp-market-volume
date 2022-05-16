from app.features.collections.page import page
from app.features.collections.service import CollectionsService
from sdk.services.client_service import ClientService
from sdk.ui.components import selected_currency

COLLECTION_NAME = "collections"


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
            'Collections',
            self.path
        )
        await self.client_service.emit_page(
            sid,
            self.path,
            page(COLLECTION_NAME)
        )

    async def on_client_state_changed(self, sid, event):
        await self.client_service.emit_busy(sid, COLLECTION_NAME)
        
        currency = selected_currency(event)

        documents = self.collections_service.get_documents(currency)

        await self.client_service.emit_documents(
            sid,
            COLLECTION_NAME,
            documents
        )

        await self.client_service.emit_done(sid, COLLECTION_NAME)
