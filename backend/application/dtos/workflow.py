from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass(frozen=False)
class WorkflowStepCommand(ABC):
    name: str

@dataclass(frozen=False)
class WorkflowCommand(ABC):
    workflow_id: str
    workflow_name: str
    steps: Optional[list[WorkflowStepCommand]]

@dataclass(frozen=False)
class SyncPennyLaneWorkflowCommand(WorkflowCommand):
    provider: str
    
    def to_dict_mapping(
        self,
    ) -> dict:
        return {
            "workflow_id":self.workflow_id,
            "workflow_name":self.workflow_name,
            "provider":self.provider
        }
    
    def as_dict(
        self,
    ) -> dict:
        return asdict(self)