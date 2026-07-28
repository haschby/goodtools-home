from dependency_injector import containers, providers
from infrastructure.gateways.goodcollectGateway import GoodcollectGateway

class GCContainer(containers.DeclarativeContainer):
    
    session = providers.Dependency()
    logger = providers.Dependency()
    
    goodcollect_gateway = providers.Factory(
        GoodcollectGateway,
        session=session,
        logger=logger
    )