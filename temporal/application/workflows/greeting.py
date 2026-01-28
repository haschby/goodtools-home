
from dataclasses import dataclass
from datetime import timedelta
from temporalio import workflow


with workflow.unsafe.imports_passed_through():
    import asyncio
    from application.activities.SayHello import SayHelloActivity

@dataclass
class GreetingWorkflowProps:
    name: str

@workflow.defn
class GreetingWorkflow():
    
    
    props: GreetingWorkflowProps = None
    greetings: asyncio.Queue[str] = asyncio.Queue()
    _exit = False
    
    @workflow.run
    async def run(self, props: GreetingWorkflowProps) -> str:
        self.props = props
        await workflow.wait_condition(lambda: self._exit)
    
    @workflow.signal(name="Fetch Data Pennylane")
    async def pennylane_signal(self) -> None:
        print('pennylane_signal received', self.props)
        self.props.name = 'Engineer new name'
        # self._exit = Tru
    
    @workflow.signal(name="OCR Fetched Data")
    async def ocr_signal(self) -> None:
        print('ocr_signal received', self.props)
        await workflow.sleep(timedelta(seconds=10))
        
    @workflow.signal(name="Store Data in Database")
    async def store_data_in_database_signal(self) -> None:
        print('store_data_in_database_signal received', self.props)
        await workflow.sleep(timedelta(seconds=10))
        
    @workflow.signal(name="Invoice Validated")
    async def invoice_validated_signal(self) -> None:
        print('invoice_validated_signal received', self.props)
        self._exit = True