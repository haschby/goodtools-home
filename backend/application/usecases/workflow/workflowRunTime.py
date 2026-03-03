class WorkflowRunTime:
    
    def __init__(
        self,
        get_workflow_usecase: GetWorkflowUsecase,
        update_workflow_usecase: UpdateWorkflowUsecase
    ) -> None:
        self.get_workflow_usecase = get_workflow_usecase
        self.update_workflow_usecase = update_workflow_usecase
    
    
    