from dependency_injector import containers, providers
# from redis.asyncio import redis

from infrastructure.config.settings import settings
from infrastructure.db.engine import AsyncSessionLocal
from infrastructure.gateways.GrokGateway import GrokGateway
from infrastructure.storage.minioStorage import MinioStorage
from infrastructure.db.workflowRepository import WorkflowRepositoryImpl
from infrastructure.gateways.accounting.pennylane import PennyLaneAccountingGateway
from infrastructure.logger.logger import LoggerImplement

# from application.containers.openAIContainer import OpenAIContainer
from application.containers.invoiceContainer import InvoiceContainer
# from application.containers.ocrContainer import OCRContainer
from application.containers.userContainer import UserContainer
from application.containers.orchestrator.orchestratorContainer import OrchestratorContainer
from application.containers.workflowContainer import WorkflowContainer
from application.containers.orchestrator.activitiesContainer import ActivitiesContainer



class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["infrastructure.routes"]
    )
    
    config = providers.Configuration()
    config.from_pydantic(settings)
    
    logger = providers.Factory(
        LoggerImplement,
        systemLogger="Goodtools.Application"
    )
    
    # # LAUNCH OF THE DATABASE SESSION
    # # THIS IS A RESOURCE BECAUSE IT IS A CONTEXT MANAGER
    session_factory = providers.Factory(
        lambda: AsyncSessionLocal()
    )
    
    pennylane_gateway = providers.Resource(
        PennyLaneAccountingGateway,
        api_token=config.pennylane_api_token(),
        api_url=config.pennylane_api_public_url()
    )
    # redis_client = providers.Resource(
    #     lambda: redis.Redis(
    #         host=config.redis_host(),
    #         port=config.redis_port(),
    #         decode_responses=True
    #     )
    # )   
    
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
        storage=minioClient,
        session=session_factory,
        pennylane_gateway=pennylane_gateway,
        logger=logger
    )
    
    # invoice_usecases = {
    #     "createInvoiceUsecase": invoice_container.createInvoiceUsecase,
    #     "getInvoiceUsecase": invoice_container.getInvoiceUsecase,
    #     "updateInvoiceUsecase": invoice_container.updateInvoiceUsecase,
    #     "getAllInvoicesUsecase": invoice_container.getAllInvoicesUsecase,
    # }
    
    # openai_container = providers.Container(
    #     OpenAIContainer,
    #     grokClient=grokClient
    # )
    
    # ocr_container = providers.Container(
    #     OCRContainer,
    #     invoice_usecases=invoice_usecases,
    #     storage=minioClient,
    #     openaiClient=grokClient
    # )
    
    user_container = providers.Container(
        UserContainer,
        postgres=session_factory
    )
    
    workflow_container = providers.Container(
        WorkflowContainer,
        session=session_factory,
        logger=logger
    )
    
    activities_container = providers.Container(
        ActivitiesContainer,
        pennylane_gateway=pennylane_gateway,
        invoice_container=invoice_container,
        workflow_container=workflow_container,
        storage=minioClient,
    )
    
    orchestrator_container = providers.Container(
        OrchestratorContainer,
        pennylane_gateway=pennylane_gateway,
        invoice_container=invoice_container,
        workflow_container=workflow_container,
        activities_container=activities_container,
        storage=minioClient,
    )
    
    