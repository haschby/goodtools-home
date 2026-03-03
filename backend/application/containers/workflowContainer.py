from dependency_injector import containers, providers
from infrastructure.proxies.loggerProxy import LoggedRepoProxy
from infrastructure.db.workflowRepository import WorkflowRepositoryImpl

from application.usecases.workflow.createWorkflow import CreateWorkflow
from application.usecases.workflow.updateWorkflow import UpdateWorkflow
from application.usecases.workflow.getWorkflows import GetWorkflows
from application.usecases.workflow.getWorkflow import GetWorkflow
from application.facades.workflowFacade import WorkflowFacade



class WorkflowContainer(containers.DeclarativeContainer):
    
    session = providers.Dependency()
    logger = providers.Dependency()
    
    repository = providers.Factory(
        WorkflowRepositoryImpl,
        session=session
    )
    
    logged_repository = providers.Factory(
        LoggedRepoProxy,
        repo=repository,
        logger=logger
    )
    
    createWorkflowUsecase = providers.Factory(
        CreateWorkflow,
        repository=logged_repository
    )
    
    updateWorkflowUsecase = providers.Factory(
        UpdateWorkflow,
        repository=logged_repository
    )
    
    getWorkflowsUsecase = providers.Factory(
        GetWorkflows,
        repository=logged_repository
    )
    
    getWorkflowUsecase = providers.Factory(
        GetWorkflow,
        repository=logged_repository
    )
    
    workflowFacade = providers.Factory(
        WorkflowFacade,
        createWorkflowUsecase=createWorkflowUsecase,
        updateWorkflowUsecase=updateWorkflowUsecase,
        getWorkflowsUsecase=getWorkflowsUsecase,
        getWorkflowUsecase=getWorkflowUsecase
    )