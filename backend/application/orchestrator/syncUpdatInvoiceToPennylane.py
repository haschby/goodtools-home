from application.ports.orchestrator.baseActivity import BaseActivity
from application.dtos.workflow import SyncUpdateInvoiceToPennylaneCommand, WorkflowStepCommand
from domain.models.workflow import Workflow, StatusWorkflow
from datetime import datetime
import json

class SyncUpdateInvoiceToPennylaneError(Exception):
    pass

class SyncUpdateInvoiceToPennylane(BaseActivity):
    
    workflows: dict[str, Workflow]
    
    def __init__(
        self,
        create_workflow_usecase: BaseActivity,
        search_invoice_usecase: BaseActivity,
        update_workflow_usecase: BaseActivity,
        update_pennylane_supplier_invoice_usecase: BaseActivity
    ) -> None:
        self.create_workflow = create_workflow_usecase
        self.search_invoice = search_invoice_usecase
        self.update_workflow = update_workflow_usecase
        self.update_pennylane_supplier_invoice = update_pennylane_supplier_invoice_usecase
        self.workflows = {}  # Initialize the workflows dictionary
        
    async def execute(self, command: SyncUpdateInvoiceToPennylaneCommand) -> bool:
        workflow = None  # Initialize to ensure it exists in except block
        
        try:
            command.steps = [
                WorkflowStepCommand(
                    name="get_external_invoice_id"
                ),
                WorkflowStepCommand(
                    name="update_pennylane_supplier_invoice"
                )
            ]
            workflow = await self.create_workflow.execute(command)
            self.workflows.setdefault(workflow.id, workflow)

            external_invoice_id = await self.search_invoice.execute(command.invoice_id)
            if external_invoice_id and not external_invoice_id['data']:
                workflow.steps[0].status = StatusWorkflow.FAILED  
                workflow.steps[0].ended_at = datetime.now()
                workflow.steps[0].message = "No invoice found"
                workflow.status = StatusWorkflow.ABORT
                workflow.ended_at = datetime.now()
                workflow.params = {
                    **(workflow.params or {}),
                    "external_invoice_id": None
                }
                self.workflows[workflow.id] = workflow
                raise SyncUpdateInvoiceToPennylaneError("No invoice found")
            
            workflow.steps[0].status = StatusWorkflow.COMPLETED
            workflow.steps[0].ended_at = datetime.now()
            workflow.steps[0].message = "External invoice id found"
            workflow.params = {
                **(workflow.params or {}),
                "data": external_invoice_id['data'][0].model_dump(mode='json')
            }
            self.workflows[workflow.id] = workflow
            
            try:
                success = await self.update_pennylane_supplier_invoice.execute(external_invoice_id['data'][0].external_id)
            except Exception as e:
                workflow.steps[1].status = StatusWorkflow.FAILED
                workflow.steps[1].ended_at = datetime.now()
                raise SyncUpdateInvoiceToPennylaneError(str(e))
            
            if not success:
                workflow.steps[1].status = StatusWorkflow.FAILED
                workflow.steps[1].ended_at = datetime.now()
                workflow.steps[1].message = str(success)
                workflow.status = StatusWorkflow.FAILED
                workflow.ended_at = datetime.now()
                workflow.params = {
                    **(workflow.params or {}),
                    "success": str(success)
                }
                raise SyncUpdateInvoiceToPennylaneError(f"Failed to update invoice to pennylane: {json.dumps(success, indent=4)}")
            
            workflow.steps[1].status = StatusWorkflow.COMPLETED
            workflow.steps[1].ended_at = datetime.now()
            workflow.steps[1].message = "Invoice updated to pennylane"
            workflow.status = StatusWorkflow.COMPLETED
            workflow.ended_at = datetime.now()
            self.workflows[workflow.id] = workflow
            
            return True
        
        except Exception as e:
            if workflow:
                for step in workflow.steps:
                    if step.status not in [
                        StatusWorkflow.COMPLETED, 
                        StatusWorkflow.SKIP, 
                        StatusWorkflow.FAILED,
                        StatusWorkflow.ABORT
                    ]:
                        step.status = StatusWorkflow.FAILED
                        step.ended_at = datetime.now()
                        if not step.message:
                            step.message = str(e)
                
                workflow.message = f"Failed to process workflow: {str(e)}"
                workflow.status = StatusWorkflow.FAILED
                workflow.ended_at = datetime.now()
                self.workflows[workflow.id] = workflow
            
            return False
        
        finally:
            if self.workflows:
                await self.update_workflow.execute(list(self.workflows.values()))