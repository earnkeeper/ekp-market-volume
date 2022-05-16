from app.features.collections.page import page
from app.features.collections.service import CollectionsService
from sdk.services.client_service import ClientService

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
        client_service.add_controller(self)

    async def on_connect(self, sid):
        self.client_service.emit_menu(
            sid,
            'bar-chart',
            'Collections',
            self.path
        )
        self.client_service.emit_page(
            sid,
            self.path,
            page(COLLECTION_NAME)
        )

    async def on_client_state_changed(self, sid, event):
        self.client_service.emit_busy(sid, COLLECTION_NAME)

        documents = self.collections_service.get_documents()

        self.client_service.emit_documents(
            sid,
            COLLECTION_NAME,
            documents
        )

        self.client_service.emit_done(sid, COLLECTION_NAME)
