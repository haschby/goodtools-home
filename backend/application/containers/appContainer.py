from dependency_injector import containers, providers

from infrastructure.config.settings import Settings, DatabaseSchema
from infrastructure.db.engine import Database
from infrastructure.gateways.GrokGateway import GrokGateway
from infrastructure.storage.minioStorage import MinioStorage
from infrastructure.db.workflowRepository import WorkflowRepositoryImpl
from infrastructure.gateways.accounting.pennylane import PennyLaneAccountingGateway
from infrastructure.logger.logger import LoggerImplement

from application.containers.invoiceContainer import InvoiceContainer
from application.containers.buybackContainer import BuybackContainer
from application.containers.userContainer import UserContainer
from application.containers.orchestrator.orchestratorContainer import OrchestratorContainer
from application.containers.workflowContainer import WorkflowContainer
from application.containers.orchestrator.activitiesContainer import ActivitiesContainer
from application.containers.gcContainer import GCContainer



class AppContainer(containers.DeclarativeContainer):
    
    wiring_config = containers.WiringConfiguration(
        packages=["infrastructure.routes"]
    )
    
    settings = providers.Singleton(Settings)    
    
    logger = providers.Factory(
        LoggerImplement,
        systemLogger="Goodtools.Application"
    )
    
    # # LAUNCH OF THE DATABASE SESSION
    # # THIS IS A RESOURCE BECAUSE IT IS A CONTEXT MANAGER
    # session_factory = providers.Object(AsyncSessionLocal)
    
    main_database_schema = providers.Callable(
        DatabaseSchema,
        db_user=settings.provided.db_user,
        db_pass=settings.provided.db_pass,
        db_host=settings.provided.db_host,
        db_port=settings.provided.db_port,
        db_name=settings.provided.db_name
    )
    
    gc_database_schema = providers.Callable(
        DatabaseSchema,
        db_user=settings.provided.gc_db_user,
        db_pass=settings.provided.gc_db_pass,
        db_host=settings.provided.gc_db_host,
        db_port=settings.provided.gc_db_port,
        db_name=settings.provided.gc_db_name
    )
    
    main_database_uri = main_database_schema.provided.build_database_uri.call()
    gc_database_uri = gc_database_schema.provided.build_database_uri.call()
    
    main_db_uri = providers.Resource(
        Database, 
        database_uri=main_database_uri
    )
    gc_db_uri = providers.Resource(
        Database,
        database_uri=gc_database_uri,
        extra_args={"server_settings": {"search_path": "public"}}
    )
    
    pennylane_gateway = providers.Resource(
        PennyLaneAccountingGateway,
        api_token=settings().pennylane_api_token,
        api_url=settings().pennylane_api_public_url
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
        api_key=settings().grok_api_key,
        model=settings().grok_api_model
    )
    
    #STORAGE CLIENT
    minioClient = providers.Resource(
        MinioStorage,
        host=settings().minio_host,
        access_key=settings().minio_access_key,
        secret_key=settings().minio_secret_key,
        bucket_name=settings().minio_bucket,
        region=settings().minio_region,
    )
    
    goodcollect_container = providers.Container(
        GCContainer,
        session=gc_db_uri.provided.session_factory,
        logger=logger
    )
    
    invoice_container = providers.Container(
        InvoiceContainer,
        storage=minioClient,
        session=main_db_uri.provided.session_factory,
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
        postgres=main_db_uri.provided.session_factory
    )
    
    workflow_container = providers.Container(
        WorkflowContainer,
        session=main_db_uri.provided.session_factory,
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
        main_session=main_db_uri.provided.session_factory,
        pennylane_gateway=pennylane_gateway,
        invoice_container=invoice_container,
        workflow_container=workflow_container,
        activities_container=activities_container,
        storage=minioClient,
        goodcollect_gateway=goodcollect_container.goodcollect_gateway,
    )
    
    buyback_container = providers.Container(
        BuybackContainer,
        session=main_db_uri.provided.session_factory,
        storage=minioClient,
        workflow_launcher=orchestrator_container.localWorkflowLauncher,
    )
    
    