from application.usecases.workflow.createWorkflow import CreateWorkflow
from application.usecases.workflow.updateWorkflow import UpdateWorkflow
from application.usecases.workflow.getWorkflows import GetWorkflows
from application.usecases.workflow.getWorkflow import GetWorkflow

class WorkflowFacade:
    def __init__(self,
        createWorkflowUsecase: CreateWorkflow,
        updateWorkflowUsecase: UpdateWorkflow,
        getWorkflowsUsecase: GetWorkflows,
        getWorkflowUsecase: GetWorkflow
    ):
        self.createWorkflowUsecase = createWorkflowUsecase
        self.updateWorkflowUsecase = updateWorkflowUsecase
        self.getWorkflowsUsecase = getWorkflowsUsecase
        self.getWorkflowUsecase = getWorkflowUsecase