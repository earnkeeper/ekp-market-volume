from ekp_sdk import BaseContainer

from app.features.collections.controller import CollectionsController
from app.features.collections.service import CollectionsService
from db.contract_volumes_repo import ContractVolumesRepo
from decouple import config

class AppContainer(BaseContainer):
    def __init__(self):
        # TODO: this is needed to fix a quirk of the decouple library, don't remove it
        POSTGRES_URI = config("POSTGRES_URI")
        
        super().__init__()

        # DB

        self.contract_volumes_repo = ContractVolumesRepo(
            pg_client=self.pg_client,
        )

        # FEATURES

        self.collections_service = CollectionsService(
            contract_volumes_repo=self.contract_volumes_repo
        )

        self.collections_controller = CollectionsController(
            client_service=self.client_service,
            collections_service=self.collections_service
        )


if __name__ == '__main__':
    container = AppContainer()

    container.client_service.add_controller(container.collections_controller)

    container.client_service.listen()
