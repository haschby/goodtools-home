import logging
from datetime import datetime
from typing import Callable

from application.ports.orchestrator.baseActivity import BaseActivity
from application.dtos.workflow import SyncBuybackToGcCommand, WorkflowStepCommand
from domain.models.workflow import Workflow, StatusWorkflow
from domain.models.goodtool import Asset, RentabilityBooking

from infrastructure.db.workflowRepository import WorkflowRepositoryImpl
from application.usecases.workflow.createWorkflow import CreateWorkflow
from application.usecases.workflow.updateWorkflow import UpdateWorkflow
from application.orchestrator.activities.createWorkflowSync import CreateWorkflowSync
from application.orchestrator.activities.updateWorkflowSync import UpdateWorkflowSync

logger = logging.getLogger("Goodtools.Application")


class SyncBuybackToGcError(Exception):
    pass


class SyncBuybackToGcWorkflow(BaseActivity):
    """Synchronise a validated buyback into the GoodCollect database.

    It creates the Asset (the buyback document) then the associated
    BookingRentabilityLine so that the buyback amount is reflected on the
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

    async def execute(self, command: SyncBuybackToGcCommand) -> bool:
        try:
            return await self._run(command)
        except Exception:
            logger.exception("SyncBuybackToGcWorkflow failed")
            return False

    async def _run(self, command: SyncBuybackToGcCommand) -> bool:
        create_workflow, update_workflow = self._build_workflow_usecases()
        workflow = None

        try:
            command.steps = [
                WorkflowStepCommand(name="create_gc_asset"),
                WorkflowStepCommand(name="create_gc_rentability_line"),
            ]
            workflow = await create_workflow.execute(command)

            asset = await self.goodcollect_gateway.createAsset(
                Asset(
                    fileKey=command.file_path or command.buyback_id,
                    fileUrl=command.file_path or "",
                )
            )
            asset_id = asset["id"]

            workflow.steps[0].status = StatusWorkflow.COMPLETED
            workflow.steps[0].ended_at = datetime.now()
            workflow.steps[0].message = f"GC asset created: {asset_id}"
            workflow.params = {**(workflow.params or {}), "gc_asset_id": asset_id}
            await update_workflow.execute(workflow)

            rentability = await self.goodcollect_gateway.createRentabilityBooking(
                RentabilityBooking(
                    bookingId=int(command.gc_booking),
                    assetId=asset_id,
                    priceHT=command.amount,
                )
            )

            workflow.steps[1].status = StatusWorkflow.COMPLETED
            workflow.steps[1].ended_at = datetime.now()
            workflow.steps[1].message = f"GC rentability line created: {rentability['id']}"
            workflow.params = {
                **(workflow.params or {}),
                "gc_rentability_line_id": rentability["id"],
            }
            workflow.status = StatusWorkflow.COMPLETED
            workflow.ended_at = datetime.now()
            workflow.message = "Buyback synchronized to GoodCollect"
            await update_workflow.execute(workflow)
            return True

        except Exception as e:
            logger.exception("SyncBuybackToGcWorkflow._run failed")
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
                            step.message = str(e)

                workflow.message = f"Failed to sync buyback to GC: {str(e)}"[:255]
                workflow.status = StatusWorkflow.FAILED
                workflow.ended_at = datetime.now()
                try:
                    await update_workflow.execute(workflow)
                except Exception:
                    logger.exception("Failed to persist failed workflow state")
            return False

