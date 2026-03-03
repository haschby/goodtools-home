from asyncio import Semaphore, TaskGroup, sleep
from datetime import datetime

from application.ports.providers.accountingGateway import AccountingGateway
from application.ports.baseUsecase import BaseUsecase
from application.dtos.workflow import WorkflowCommand, WorkflowStepCommand
from domain.models.workflow import StatusWorkflow, Workflow
from application.dtos.invoiceDto import InvoiceResponseSchema

class SyncPennyLaneWorkflow(BaseUsecase):
    
    semaphore = Semaphore(2)
    task_group = TaskGroup()
    invoices = []
    
    def __init__(self,
        create_workflow_usecase: BaseUsecase,
        update_workflow_usecase: BaseUsecase,
        fetch_pennylane_supplier_invoices_usecase: BaseUsecase,
        store_pdf_invoice_usecase: BaseUsecase,
        create_invoice_usecase: BaseUsecase
    ) -> None:
        self.create_workflow_usecase = create_workflow_usecase
        self.update_workflow_usecase = update_workflow_usecase
        self.fetch_pennylane_usecase = fetch_pennylane_supplier_invoices_usecase
        self.store_pdf_invoice_usecase = store_pdf_invoice_usecase
        self.create_invoice_usecase = create_invoice_usecase
        
    async def _process_invoice(self, invoice_data: InvoiceResponseSchema) -> None:
        print("@Processing invoice started", invoice_data.name)
        
        pdf_url = invoice_data.path
        invoice_name = invoice_data.name
        
        try:
            pdf_file_id = await self.store_pdf_invoice_usecase.execute(pdf_url, invoice_name)
            invoice_data.path = pdf_file_id
        except Exception as e:
            print('@ERROR', e)
        finally:
            self.invoices.append(invoice_data)
            return invoice_data
        
    async def execute(self, command: WorkflowCommand) -> None:
        """
            Start a workflow
            - Fetch data from provider
            - OCR data
            - Store data in database
        """
        command.steps = [
            WorkflowStepCommand(
                name="fetch_pennylane_supplier_invoices"
            )
        ]
        workflow = await self.create_workflow_usecase.execute(command)
        
        invoices = await self.fetch_pennylane_usecase.execute()
        if not invoices:
            workflow.steps[0].status = StatusWorkflow.SKIP  
            workflow.steps[0].ended_at = datetime.now()
            workflow.steps[0].message = "No invoices to process"
            workflow.status = StatusWorkflow.ABORT
            workflow.ended_at = datetime.now()
            workflow.params = {
                **(workflow.params or {}),
                "fetched_invoices": []
            }
            workflow.message = "Workflow Aborted due to no matching invoices"
            await self.update_workflow_usecase.execute(workflow)
            return
        
        
        workflow.steps[0].status = StatusWorkflow.COMPLETED
        workflow.steps[0].ended_at = datetime.now()
        await self.update_workflow_usecase.execute(workflow)
        self.invoices = invoices
        
        # async def guarded_process(invoice):
        #     async with self.semaphore:
        #         return await self._process_invoice(invoice)
            
        # async with TaskGroup() as tg:
        #     for invoice in invoices:
        #         tg.create_task(guarded_process(invoice))
        
        invoice_ids = [invoice.external_id for invoice in invoices]        
        unique_invoices = list({inv.external_id: inv for inv in self.invoices}.values()) if self.invoices else []
        await self.create_invoice_usecase.execute(unique_invoices)
        
        workflow.status = StatusWorkflow.COMPLETED
        workflow.ended_at = datetime.now()
        workflow.message = "Workflow Completed with success"
        workflow.params = {
            **(workflow.params or {}),
            "fetched_invoices": invoice_ids
        }
        await self.update_workflow_usecase.execute(workflow)