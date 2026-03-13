from datetime import datetime
from typing import Callable
import json

from application.ports.orchestrator.baseActivity import BaseActivity
from application.dtos.workflow import SyncUpdateInvoiceToPennylaneCommand, WorkflowStepCommand
from domain.models.workflow import Workflow, StatusWorkflow

from infrastructure.db.workflowRepository import WorkflowRepositoryImpl
from application.usecases.workflow.createWorkflow import CreateWorkflow
from application.usecases.workflow.updateWorkflow import UpdateWorkflow
from application.orchestrator.activities.createWorkflowSync import CreateWorkflowSync
from application.orchestrator.activities.updateWorkflowSync import UpdateWorkflowSync


class SyncUpdateInvoiceToPennylaneError(Exception):
    pass


class SyncUpdateInvoiceToPennylane(BaseActivity):

    def __init__(
        self,
        session_factory: Callable,
        search_invoice_usecase: BaseActivity,
        update_pennylane_supplier_invoice_usecase: BaseActivity,
    ) -> None:
        self.session_factory = session_factory
        self.search_invoice = search_invoice_usecase
        self.update_pennylane_supplier_invoice = update_pennylane_supplier_invoice_usecase

    def _build_workflow_usecases(self, session):
        repo = WorkflowRepositoryImpl(session)
        return (
            CreateWorkflowSync(CreateWorkflow(repo)),
            UpdateWorkflowSync(UpdateWorkflow(repo))
        )

    async def execute(self, command: SyncUpdateInvoiceToPennylaneCommand) -> bool:
        async with self.session_factory() as session:
            try:
                return await self._run(command, session)
            except Exception:
                await session.rollback()
                return False

    async def _run(self, command: SyncUpdateInvoiceToPennylaneCommand, session) -> bool:
        create_workflow, update_workflow = self._build_workflow_usecases(session)
        local_workflows: dict[str, Workflow] = {}
        workflow = None

        try:
            command.steps = [
                WorkflowStepCommand(name="get_external_invoice_id"),
                WorkflowStepCommand(name="update_pennylane_supplier_invoice")
            ]
            workflow = await create_workflow.execute(command)
            await session.commit()
            local_workflows[workflow.id] = workflow

            external_invoice_id = await self.search_invoice.execute(command.invoice_id)
            if external_invoice_id and not external_invoice_id['data']:
                workflow.steps[0].status = StatusWorkflow.FAILED
                workflow.steps[0].ended_at = datetime.now()
                workflow.steps[0].message = "No invoice found"
                workflow.status = StatusWorkflow.ABORT
                workflow.ended_at = datetime.now()
                workflow.params = {**(workflow.params or {}), "external_invoice_id": None}
                local_workflows[workflow.id] = workflow
                raise SyncUpdateInvoiceToPennylaneError("No invoice found")

            workflow.steps[0].status = StatusWorkflow.COMPLETED
            workflow.steps[0].ended_at = datetime.now()
            workflow.steps[0].message = "External invoice id found"
            workflow.params = {
                **(workflow.params or {}),
                "data": external_invoice_id['data'][0].model_dump(mode='json')
            }
            local_workflows[workflow.id] = workflow

            try:
                success = await self.update_pennylane_supplier_invoice.execute(
                    external_invoice_id['data'][0].external_id
                )
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
                workflow.params = {**(workflow.params or {}), "success": str(success)}
                local_workflows[workflow.id] = workflow
                raise SyncUpdateInvoiceToPennylaneError(
                    f"Failed to update invoice to pennylane: {json.dumps(success, indent=4)}"
                )

            workflow.steps[1].status = StatusWorkflow.COMPLETED
            workflow.steps[1].ended_at = datetime.now()
            workflow.steps[1].message = "Invoice updated to pennylane"
            workflow.status = StatusWorkflow.COMPLETED
            workflow.ended_at = datetime.now()
            local_workflows[workflow.id] = workflow
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
                local_workflows[workflow.id] = workflow
            return False

        finally:
            if local_workflows:
                await update_workflow.execute(list(local_workflows.values()))
                await session.commit()