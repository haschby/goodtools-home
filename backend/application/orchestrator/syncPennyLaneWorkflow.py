from asyncio import Semaphore
from datetime import datetime
from typing import Callable

from application.ports.baseUsecase import BaseUsecase
from application.dtos.workflow import WorkflowCommand, WorkflowStepCommand
from domain.models.workflow import StatusWorkflow
from application.dtos.invoiceDto import InvoiceResponseSchema

from infrastructure.db.workflowRepository import WorkflowRepositoryImpl
from application.usecases.workflow.createWorkflow import CreateWorkflow
from application.usecases.workflow.updateWorkflow import UpdateWorkflow
from application.orchestrator.activities.createWorkflowSync import CreateWorkflowSync
from application.orchestrator.activities.updateWorkflowSync import UpdateWorkflowSync


class SyncPennyLaneWorkflowError(Exception):
    pass


class SyncPennyLaneWorkflow(BaseUsecase):

    semaphore = Semaphore(2)

    def __init__(self,
        session_factory: Callable,
        fetch_pennylane_supplier_invoices_usecase: BaseUsecase,
        store_pdf_invoice_usecase: BaseUsecase,
        create_invoice_usecase: BaseUsecase
    ) -> None:
        self.session_factory = session_factory
        self.fetch_pennylane_usecase = fetch_pennylane_supplier_invoices_usecase
        self.store_pdf_invoice_usecase = store_pdf_invoice_usecase
        self.create_invoice_usecase = create_invoice_usecase

    def _build_workflow_usecases(self, session):
        repo = WorkflowRepositoryImpl(session)
        return (
            CreateWorkflowSync(CreateWorkflow(repo)),
            UpdateWorkflowSync(UpdateWorkflow(repo))
        )

    def _deduplicate(self, invoices: list[InvoiceResponseSchema]) -> list[InvoiceResponseSchema]:
        return list({inv.external_id: inv for inv in invoices}.values())

    async def _abort_workflow(self, workflow, update_workflow, session, message: str) -> None:
        workflow.steps[0].status = StatusWorkflow.SKIP
        workflow.steps[0].ended_at = datetime.now()
        workflow.steps[0].message = message
        workflow.status = StatusWorkflow.ABORT
        workflow.ended_at = datetime.now()
        workflow.message = f"Workflow aborted: {message}"
        workflow.params = {**(workflow.params or {}), "fetched_invoices": []}
        await update_workflow.execute(workflow)
        await session.commit()

    async def _complete_step(self, workflow, update_workflow, session) -> None:
        workflow.steps[0].status = StatusWorkflow.COMPLETED
        workflow.steps[0].ended_at = datetime.now()
        await update_workflow.execute(workflow)
        await session.commit()

    async def _complete_workflow(self, workflow, update_workflow, session, invoice_ids: list[str]) -> None:
        workflow.status = StatusWorkflow.COMPLETED
        workflow.ended_at = datetime.now()
        workflow.message = "Workflow completed with success"
        workflow.params = {**(workflow.params or {}), "fetched_invoices": invoice_ids}
        await update_workflow.execute(workflow)
        await session.commit()

    async def execute(self, command: WorkflowCommand) -> None:
        async with self.session_factory() as session:
            try:
                await self._run(command, session)
            except Exception as e:
                await session.rollback()
                raise SyncPennyLaneWorkflowError(str(e)) from e

    async def _run(self, command: WorkflowCommand, session) -> None:
        create_workflow, update_workflow = self._build_workflow_usecases(session)

        command.steps = [WorkflowStepCommand(name="fetch_pennylane_supplier_invoices")]
        workflow = await create_workflow.execute(command)
        await session.commit()

        invoices = await self.fetch_pennylane_usecase.execute()
        if not invoices:
            await self._abort_workflow(workflow, update_workflow, session, "No invoices to process")
            return

        await self._complete_step(workflow, update_workflow, session)

        unique_invoices = self._deduplicate(invoices)
        await self.create_invoice_usecase.execute(unique_invoices)

        await self._complete_workflow(
            workflow, update_workflow, session,
            invoice_ids=[inv.external_id for inv in invoices]
        )