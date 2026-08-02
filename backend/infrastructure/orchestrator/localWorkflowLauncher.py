import asyncio

from application.ports.orchestrator.workflowLauncher import WorkflowLauncher
from application.ports.baseUsecase import BaseUsecase
from application.dtos.workflow import WorkflowCommand
from typing import Dict, List

class LocalWorkflowLauncher(WorkflowLauncher):
    
    workflows_to_start: List[WorkflowCommand] = []
    def __init__(self, workflows: Dict[[str], BaseUsecase]) -> None:
        self._workflows = workflows
    
    def registerWorkflows(self, commands: List[WorkflowCommand]) -> None:
        self.workflows_to_start.extend(commands)
    
    async def launchWorkflows(self) -> None:
        for command in self.workflows_to_start:
            await self.startWorkflow(command)
        self.workflows_to_start = []
    
    async def startWorkflow(self, command: WorkflowCommand) -> None:
        workflow = self._workflows[command.workflow_name]
        asyncio.create_task(
            workflow.execute(command)
        )