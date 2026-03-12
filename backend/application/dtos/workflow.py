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
    
    def as_dict(
        self,
    ) -> dict:
        return asdict(self)
    
    def to_dict_mapping(
        self,
    ) -> dict:
        return {
            "workflow_id":self.workflow_id,
            "workflow_name":self.workflow_name,
            "provider":self.provider,
            "steps":self.steps
        }
    

@dataclass(frozen=False)
class SyncPennyLaneWorkflowCommand(WorkflowCommand):
    provider: str
    steps: Optional[list[WorkflowStepCommand]]
    
    
    
@dataclass(frozen=False)
class SyncUpdateInvoiceToPennylaneCommand(WorkflowCommand):
    invoice_id: str