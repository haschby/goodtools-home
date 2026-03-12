from fastapi import APIRouter, Depends, Request, BackgroundTasks
from dependency_injector.wiring import inject, Provide
from application.containers.appContainer import AppContainer
from application.ports.baseRepository import BaseRepositoryPort
from application.ports.baseUsecase import BaseUsecase
from application.ports.orchestrator.workflowLauncher import WorkflowLauncher
from application.dtos.workflow import SyncPennyLaneWorkflowCommand

def workflow_routes() -> APIRouter:
    
    router = APIRouter(
        prefix="/client/workflow",
        tags=["workflow"]
    )
    
    @router.get("/",
        operation_id="get_workflows",
        status_code=201
    )
    @inject
    async def get_workflows(
        getWorkflowsUsecase: BaseUsecase = Depends(
            Provide[AppContainer.workflow_container.getWorkflowsUsecase]
        )
    ):
        return await getWorkflowsUsecase.execute()
    
    @router.get("/poll/{id:str}",
        operation_id="pull_workflow_id",
        status_code=201
    )
    @inject
    async def pull_workflow_id(
        id: str,
        getWorkflowUsecase: BaseUsecase = Depends(
            Provide[AppContainer.workflow_container.getWorkflowUsecase]
        )
    ):
        print('@POLL_WORKFLOW_ID', id)
        return await getWorkflowUsecase.execute(id)
    
    @router.post("/{provider:str}/{id:str}/start",
        operation_id="start_workflow",
        status_code=201
    )
    @inject
    async def start_workflow(
        id: str,
        provider: str,
        request: Request,
        background_tasks: BackgroundTasks,
        orchestrator: WorkflowLauncher = Depends(
            Provide[AppContainer.orchestrator_container.localWorkflowLauncher]
        )
    ):
        workflow_name = request.headers.get('workflow-name')
        command = SyncPennyLaneWorkflowCommand(
            workflow_name=workflow_name,
            workflow_id=id,
            provider=provider,
            steps=[]
        )
        
        background_tasks.add_task(orchestrator.startWorkflow, command)
        
        return { "message": "Workflow started", "status_code": 201 }
        
    
    return router