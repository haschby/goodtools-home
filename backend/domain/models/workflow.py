from .baseModel import BaseModel
from .columns import StringColumn, EnumColumn, ForeignKeyColumn, DateTimeColumn, JSONBColumn
from enum import Enum
from datetime import datetime
from sqlalchemy.orm import Relationship
import json

class StatusWorkflow(Enum):
    PENDING = "Pending"
    PROCESSING = "Processing"
    COMPLETED = "Completed"
    FAILED = "Failed"
    SKIP = "Skipped"
    ABORT = "Aborted"
    
class Workflow(BaseModel):
    prefix: str = "WF"
    
    ref_pulling: str = StringColumn(length=255, nullable=False)
    provider: str = StringColumn(length=255, nullable=False)
    status: StatusWorkflow = EnumColumn(StatusWorkflow, nullable=False, default=StatusWorkflow.PENDING)
    ended_at: datetime = DateTimeColumn()
    message: str = StringColumn(length=255, nullable=True)
    params: dict = JSONBColumn()
    
    steps: list["Workflow_Step"] = Relationship("Workflow_Step", back_populates="workflow", lazy="selectin")
    
    def __repr__(self):
        return f"Workflow(id={self.id}, ref_pulling={self.ref_pulling}, provider={self.provider}, status={self.status.value}, ended_at={self.ended_at}, message={self.message}, steps={len(self.steps)})"


class Workflow_Step(BaseModel):
    prefix: str = "WFS"
    
    workflow_id: str = ForeignKeyColumn(Workflow, nullable=False)
    name: str = StringColumn(length=255, nullable=False)
    status: StatusWorkflow = EnumColumn(StatusWorkflow, nullable=False, default=StatusWorkflow.PENDING)
    params: dict = JSONBColumn()
    message: str = StringColumn(length=255, nullable=True)
    ended_at: datetime = DateTimeColumn()
    
    workflow: "Workflow" = Relationship("Workflow", back_populates="steps")
    
    def __repr__(self):
        return f"Workflow_Step(id={self.id}, workflow_id={self.workflow_id}, name={self.name}, status={self.status.value}, params={self.params}, message={self.message}, ended_at={self.ended_at})"