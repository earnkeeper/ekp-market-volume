from decouple import AutoConfig
from ekp_sdk import BaseContainer
from app.features.collection.controller import SingleCollectionController
from app.features.collection.service import SingleCollectionsService

from app.features.collections.controller import CollectionsController
from app.features.collections.service import CollectionsService
from app.features.collections.sheets_client import SheetsClient
from db.contract_volumes_repo import ContractVolumesRepo


class AppContainer(BaseContainer):
    def __init__(self):
        config = AutoConfig(".env")
        
        SPREADSHEET_ID = config("SPREADSHEET_ID")
        
        super().__init__(config)

        self.sheets_client = SheetsClient()
        
        # DB

        self.contract_volumes_repo = ContractVolumesRepo(
            pg_client=self.pg_client,
        )

        # FEATURES

        self.collections_service = CollectionsService(
            contract_volumes_repo=self.contract_volumes_repo,
            coingecko_service=self.coingecko_service,
            sheets_client=self.sheets_client,
            sheet_id=SPREADSHEET_ID
        )
        self.collections_controller = CollectionsController(
            client_service=self.client_service,
            collections_service=self.collections_service
        )

        self.collection_service = SingleCollectionsService(
            contract_volumes_repo=self.contract_volumes_repo,
            coingecko_service=self.coingecko_service
        )
        self.collection_controller = SingleCollectionController(
            client_service=self.client_service,
            collection_service=self.collection_service
        )


if __name__ == '__main__':
    container = AppContainer()

    container.client_service.add_controller(container.collections_controller)
    container.client_service.add_controller(container.collection_controller)

    container.client_service.listen()
