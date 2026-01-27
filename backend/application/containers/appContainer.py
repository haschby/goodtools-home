from dependency_injector import containers, providers

from infrastructure.config.settings import settings
from infrastructure.db.engine import get_session
from infrastructure.gateways.GrokGateway import GrokGateway
from infrastructure.storage.minioStorage import MinioStorage

from application.containers.openAIContainer import OpenAIContainer
from application.containers.invoiceContainer import InvoiceContainer
from application.containers.ocrContainer import OCRContainer
from application.containers.userContainer import UserContainer

class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["infrastructure.routes"]
    )
    
    config = providers.Configuration()
    config.from_pydantic(settings)
    
    # # LAUNCH OF THE DATABASE SESSION
    # # THIS IS A RESOURCE BECAUSE IT IS A CONTEXT MANAGER
    session = providers.Resource(get_session)
    
    # OPENAI CLIENT
    grokClient = providers.Resource(
        GrokGateway,
        api_key=config.grok_api_key(),
        model=config.grok_api_model()
    )
    
    #STORAGE CLIENT
    minioClient = providers.Resource(
        MinioStorage,
        host=config.minio_host(),
        access_key=config.minio_access_key(),
        secret_key=config.minio_secret_key(),
        bucket_name=config.minio_bucket(),
        region=config.minio_region(),
    )
    
    invoice_container = providers.Container(
        InvoiceContainer,
        postgres=session,
        storage=minioClient
    )
    
    invoice_usecases = {
        "createInvoiceUsecase": invoice_container.createInvoiceUsecase,
        "getInvoiceUsecase": invoice_container.getInvoiceUsecase,
        "updateInvoiceUsecase": invoice_container.updateInvoiceUsecase,
        "getAllInvoicesUsecase": invoice_container.getAllInvoicesUsecase,
    }
    
    openai_container = providers.Container(
        OpenAIContainer,
        grokClient=grokClient
    )
    
    ocr_container = providers.Container(
        OCRContainer,
        invoice_usecases=invoice_usecases,
        storage=minioClient,
        openaiClient=grokClient
    )
    
    user_container = providers.Container(
        UserContainer,
        postgres=session
    )
    
    