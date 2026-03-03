from abc import ABC, abstractmethod
from application.dtos.workflow import WorkflowCommand

class WorkflowLauncher(ABC):
    @abstractmethod
    async def startWorkflow(self, command: WorkflowCommand) -> None:
        """
        Start a workflow
        """
        raise NotImplementedError
    