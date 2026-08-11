import logging
from datetime import datetime
from typing import Callable

from application.ports.orchestrator.baseActivity import BaseActivity
from application.dtos.workflow import SyncInvoiceToGcCommand, WorkflowStepCommand
from domain.models.workflow import StatusWorkflow
from domain.models.goodtool import Asset, RentabilityBooking

from infrastructure.db.workflowRepository import WorkflowRepositoryImpl
from infrastructure.db.invoiceRepository import InvoiceRepositoryImpl
from application.usecases.workflow.createWorkflow import CreateWorkflow
from application.usecases.workflow.updateWorkflow import UpdateWorkflow
from application.orchestrator.activities.createWorkflowSync import CreateWorkflowSync
from application.orchestrator.activities.updateWorkflowSync import UpdateWorkflowSync

logger = logging.getLogger("Goodtools.Application")


class SyncInvoiceToGcError(Exception):
    pass


class SyncInvoiceToGcWorkflow(BaseActivity):
    """Synchronise a validated invoice into the GoodCollect database.

    Triggered when an invoice reaches the "Valider avec paiement" status.
    It creates the Asset (the invoice document) then the associated
    BookingRentabilityLine so that the invoice amount is reflected on the
    GoodCollect booking.
    """

    def __init__(
        self,
        session_factory: Callable,
        goodcollect_gateway,
    ) -> None:
        self.session_factory = session_factory
        self.goodcollect_gateway = goodcollect_gateway

    def _build_workflow_usecases(self):
        repo = WorkflowRepositoryImpl(self.session_factory)
        return (
            CreateWorkflowSync(CreateWorkflow(repo)),
            UpdateWorkflowSync(UpdateWorkflow(repo)),
        )

    async def execute(self, command: SyncInvoiceToGcCommand) -> bool:
        try:
            return await self._run(command)
        except Exception:
            logger.exception("SyncInvoiceToGcWorkflow failed")
            return False

    async def _run(self, command: SyncInvoiceToGcCommand) -> bool:
        create_workflow, update_workflow = self._build_workflow_usecases()
        workflow = None

        try:
            command.steps = [
                WorkflowStepCommand(name="fetch_invoice"),
                WorkflowStepCommand(name="check_existing_rentability_line"),
                WorkflowStepCommand(name="create_gc_asset"),
                WorkflowStepCommand(name="upsert_gc_rentability_line"),
            ]
            workflow = await create_workflow.execute(command)

            invoice_repo = InvoiceRepositoryImpl(self.session_factory)
            invoice = await invoice_repo.get_by_id(command.invoice_id)

            if invoice is None:
                workflow.steps[0].status = StatusWorkflow.SKIP
                workflow.steps[0].ended_at = datetime.now()
                workflow.steps[0].message = f"Invoice not found: {command.invoice_id}"
                workflow.status = StatusWorkflow.ABORT
                workflow.ended_at = datetime.now()
                workflow.message = "Workflow aborted: invoice not found"
                await update_workflow.execute(workflow)
                return False

            if not invoice.gc_booking:
                workflow.steps[0].status = StatusWorkflow.SKIP
                workflow.steps[0].ended_at = datetime.now()
                workflow.steps[0].message = "Invoice has no gc_booking, nothing to sync"
                workflow.status = StatusWorkflow.ABORT
                workflow.ended_at = datetime.now()
                workflow.message = "Workflow aborted: no gc_booking on invoice"
                await update_workflow.execute(workflow)
                return False

            workflow.steps[0].status = StatusWorkflow.COMPLETED
            workflow.steps[0].ended_at = datetime.now()
            workflow.steps[0].message = f"Invoice fetched: [{invoice.id}, {invoice.gc_booking}]"
            await update_workflow.execute(workflow)

            existing_line = None
            if getattr(invoice, "crm_id", None):
                existing_line = await self.goodcollect_gateway.findRentabilityLineById(invoice.crm_id)
            if existing_line is None:
                existing_line = await self.goodcollect_gateway.findRentabilityLineByComment(invoice.id)
            workflow.steps[1].status = StatusWorkflow.COMPLETED
            workflow.steps[1].ended_at = datetime.now()
            workflow.steps[1].message = (
                f"Existing rentability line found: {existing_line['id']}"
                if existing_line
                else "No existing rentability line, will create"
            )
            await update_workflow.execute(workflow)

            if existing_line:
                # Update path: only refresh the filled-out fields, reuse the
                # existing asset. Asset creation is skipped.
                workflow.steps[2].status = StatusWorkflow.SKIP
                workflow.steps[2].ended_at = datetime.now()
                workflow.steps[2].message = "Reusing existing rentability line, no asset created"
                await update_workflow.execute(workflow)

                try:
                    rentability = await self.goodcollect_gateway.updateRentabilityBooking(
                        existing_line["id"],
                        RentabilityBooking(
                            bookingId=int(invoice.gc_booking),
                            priceHT=float(invoice.amount_ht or 0),
                        ),
                    )

                    workflow.steps[3].status = StatusWorkflow.COMPLETED
                    workflow.steps[3].ended_at = datetime.now()
                    workflow.steps[3].message = (
                        f"GC rentability line updated: {rentability['id']} "
                        f"(bookingId {existing_line['bookingId']} -> {rentability['bookingId']})"
                    )
                    workflow.params = {
                        **(workflow.params or {}),
                        "gc_rentability_line_id": rentability["id"],
                    }
                    workflow.status = StatusWorkflow.COMPLETED
                    workflow.ended_at = datetime.now()
                    workflow.message = "Invoice synchronized to GoodCollect (updated)"
                    await update_workflow.execute(workflow)
                    return True
                except Exception as e:
                    workflow.steps[3].status = StatusWorkflow.FAILED
                    workflow.steps[3].ended_at = datetime.now()
                    workflow.steps[3].message = f"Failed to update Rentability line: {str(e)}"
                    await update_workflow.execute(workflow)
                    raise UpdateRentabilityLineError(str(e))

            # Create path: create the asset, then the rentability line.
            try:

                asset = await self.goodcollect_gateway.createAsset(
                    Asset(
                        fileKey=invoice.path or invoice.name or str(invoice.id),
                        fileUrl=invoice.path or "",
                    )
                )
                asset_id = asset["id"]

                workflow.steps[2].status = StatusWorkflow.COMPLETED
                workflow.steps[2].ended_at = datetime.now()
                workflow.steps[2].message = f"GC asset created: {asset_id}"
                workflow.params = {**(workflow.params or {}), "gc_asset_id": asset_id}
                await update_workflow.execute(workflow)
            except Exception as e:
                workflow.steps[2].status = StatusWorkflow.FAILED
                workflow.steps[2].ended_at = datetime.now()
                workflow.steps[2].message = f"Failed to create asset: {str(e)}"
                await update_workflow.execute(workflow)
                raise CreateAssetError(str(e))

            try:
                rentability = await self.goodcollect_gateway.createRentabilityBooking(
                    RentabilityBooking(
                        bookingId=int(invoice.gc_booking),
                        assetId=asset_id,
                        priceHT=float(invoice.amount_ht or 0),
                        comment=invoice.id,
                    )
                )

                workflow.steps[3].status = StatusWorkflow.COMPLETED
                workflow.steps[3].ended_at = datetime.now()
                workflow.steps[3].message = f"GC rentability line created: {rentability['id']}"
                workflow.params = {
                    **(workflow.params or {}),
                    "gc_rentability_line_id": rentability["id"],
                }

                await invoice_repo.set_crm_id(invoice.id, str(rentability["id"]))

                workflow.status = StatusWorkflow.COMPLETED
                workflow.ended_at = datetime.now()
                workflow.message = "Invoice synchronized to GoodCollect (created)"
                await update_workflow.execute(workflow)
                return True

            except Exception as e:
                workflow.steps[3].status = StatusWorkflow.FAILED
                workflow.steps[3].ended_at = datetime.now()
                workflow.steps[3].message = f"Failed Rentability line: {str(e)}"
                await update_workflow.execute(workflow)
                raise CreateRentabilityLineError(str(e))

        except (
            CreateAssetError,
            CreateRentabilityLineError,
            UpdateRentabilityLineError,
            Exception
        ) as e:
            logger.exception(f"SyncInvoiceToGcWorkflow._run failed: {str(e)}")
            if workflow:
                for step in workflow.steps:
                    if step.status not in [
                        StatusWorkflow.COMPLETED,
                        StatusWorkflow.SKIP,
                        StatusWorkflow.FAILED,
                        StatusWorkflow.ABORT,
                    ]:
                        step.status = StatusWorkflow.FAILED
                        step.ended_at = datetime.now()
                        if not step.message:
                            step.message = str(e)[:255]

                workflow.message = f"Failed to sync invoice to GC: {str(e)}"[:255]
                workflow.status = StatusWorkflow.FAILED
                workflow.ended_at = datetime.now()
                try:
                    await update_workflow.execute(workflow)
                except Exception:
                    logger.exception("Failed to persist failed workflow state")
            return False

class CreateAssetError(Exception):
    pass

class CreateRentabilityLineError(Exception):
    pass

class UpdateRentabilityLineError(Exception):
    pass