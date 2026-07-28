from application.ports.baseUsecase import BaseUsecase
from application.ports.orchestrator.workflowLauncher import WorkflowLauncher
from domain.services.buybackService import BuybackService
from domain.models.enums import StatusBuyBackEnum
from application.dtos.buybackDto import BuybackDetailResponseSchema
from application.dtos.buybackDto import BuybackPatchSchema
from application.dtos.workflow import SyncBuybackToGcCommand

class PatchBuybackUsecase(BaseUsecase):
    """
    Usecase to patch a buyback
    """ 
    def __init__(
        self,
        buybackService: BuybackService,
        workflowLauncher: WorkflowLauncher,
    ):
        self.service = buybackService
        self.workflowLauncher = workflowLauncher

    async def execute(self, buyback: BuybackPatchSchema) -> BuybackDetailResponseSchema:
        try:
            patched = await self.service.patch(buyback)
        except Exception as error:
            return BuybackDetailResponseSchema(
                message=f"Buyback not patched: {error}",
                status_code=500,
                data=None,
            )

        if self.shouldUpdateGCDatabase(patched):
            await self.workflowLauncher.startWorkflow(
                SyncBuybackToGcCommand(
                    workflow_id=patched.id,
                    workflow_name="syncBuybackToGcWorkflow",
                    buyback_id=patched.id,
                    gc_booking=patched.gc_booking,
                    amount=float(patched.amount),
                    file_path=getattr(patched, "file_path", None),
                )
            )

        return BuybackDetailResponseSchema(
            message="Buyback patched successfully",
            status_code=200,
            data=patched,
        )

    def shouldUpdateGCDatabase(self, buyback) -> bool:
        """Détermine si la mise à jour du buyback doit être synchronisée vers la GC database.

        La synchronisation n'est déclenchée que lorsque le buyback est validé et
        qu'il dispose des informations nécessaires côté GoodCollect (montant + booking).
        """
        status = getattr(buyback, "status", None)
        if isinstance(status, StatusBuyBackEnum):
            status = status.value

        return (
            status == StatusBuyBackEnum.VALIDATED.value
            and getattr(buyback, "amount", None) is not None
            and bool(getattr(buyback, "gc_booking", None))
        )