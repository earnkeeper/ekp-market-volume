from decouple import config
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

from app.features.collections.controller import CollectionsController
from app.features.collections.service import CollectionsService
from db.contract_volumes_repo import ContractVolumesRepo
from sdk.db.pg_client import PgClient
from sdk.services.cache_service import CacheService
from sdk.services.client_service import ClientService
from sdk.services.coingecko_service import CoingeckoService
from sdk.services.redis_client import RedisClient
from sdk.services.rest_client import RestClient


class Container(containers.DeclarativeContainer):

    # CONFIG

    POSTGRES_URI = config("POSTGRES_URI")
    REDIS_URI = config("REDIS_URI", default="redis://localhost")
    PORT = config("PORT", default=3001, cast=int)
    EK_PLUGIN_ID = config("EK_PLUGIN_ID")

    # SDK

    redis_client = providers.Singleton(
        RedisClient,
        uri=REDIS_URI
    )

    rest_client = providers.Singleton(
        RestClient,
    )

    pg_client = providers.Singleton(
        PgClient,
        uri=POSTGRES_URI,
    )

    coingecko_service = providers.Singleton(
        CoingeckoService,
        rest_client=rest_client
    )

    cache_service = providers.Singleton(
        CacheService,
        redis_client=redis_client,
    )

    contract_volumes_repo = providers.Singleton(
        ContractVolumesRepo,
        pg_client=pg_client,
    )

    # CLIENT

    client_service = providers.Singleton(
        ClientService,
        port=PORT,
        plugin_id=EK_PLUGIN_ID
    )

    # FEATURES

    collections_service = providers.Singleton(
        CollectionsService,
    )

    collections_controller = providers.Singleton(
        CollectionsController,
        client_service=client_service,
        collections_service=collections_service
    )


@inject
def main(
    client_service: ClientService = Provide[Container.client_service]
):
    print("🚀 Application Start")
    client_service.listen()


if __name__ == '__main__':
    container = Container()
    container.wire(modules=[__name__])

    main()
