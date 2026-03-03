import asyncio

from application.ports.orchestrator.workflowLauncher import WorkflowLauncher
from application.ports.baseUsecase import BaseUsecase
from application.dtos.workflow import WorkflowCommand
from typing import Dict

class LocalWorkflowLauncher(WorkflowLauncher):
    def __init__(self, workflows: Dict[[str], BaseUsecase]) -> None:
        self._workflows = workflows
    
    async def startWorkflow(self, command: WorkflowCommand) -> None:
        workflow = self._workflows[command.workflow_name]
        asyncio.create_task(
            workflow.execute(command)
        )