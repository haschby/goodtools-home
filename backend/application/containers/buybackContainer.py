from dependency_injector import containers, providers

from infrastructure.db.buybackRepository import BuybackRepositoryImpl
from infrastructure.db.invoiceRepository import InvoiceRepositoryImpl
from domain.services.buybackService import BuybackService
from domain.services.invoiceService import InvoiceService
from application.usecases.buyback.createBuybacks import CreateBuybacks
from application.usecases.buyback.getAllBuybacks import GetAllBuybacks
from application.usecases.buyback.getBuybackById import GetBuybackById
from application.usecases.buyback.storeFiles import StoreFiles
from application.usecases.buyback.patchBuyback import PatchBuybackUsecase

class BuybackContainer(containers.DeclarativeContainer):

    session = providers.Dependency()
    storage = providers.Dependency()
    logger = providers.Dependency()
    
    workflow_launcher = providers.Dependency()

    repository = providers.Factory(
        BuybackRepositoryImpl,
        session=session,
    )
    
    invoiceRepository = providers.Factory(
        InvoiceRepositoryImpl,
        session=session,
    )
    
    service = providers.Factory(
        BuybackService,
        buybackRepository=repository,
    )
    
    invoiceService = providers.Factory(
        InvoiceService,
        invoiceRepository=invoiceRepository,
        storage=storage
    )

    createBuybacksUsecase = providers.Factory(
        CreateBuybacks,
        invoiceService=invoiceService,
    )

    getAllBuybacksUsecase = providers.Factory(
        GetAllBuybacks,
        buybackService=service,
    )

    getBuybackByIdUsecase = providers.Factory(
        GetBuybackById,
        buybackService=service,
        storage=storage,
    )

    storeFilesUsecase = providers.Factory(
        StoreFiles,
        storage=storage,
    )
    
    patchBuybackUsecase = providers.Factory(
        PatchBuybackUsecase,
        buybackService=service,
        workflowLauncher=workflow_launcher,
    )
