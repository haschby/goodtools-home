import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

from application.workflows.greeting import GreetingWorkflow
from application.activities.SayHello import SayHelloActivity

async def start_worker() -> None:
    client = await Client.connect("localhost:7233", namespace="default")
    
    sayHelloActivity = SayHelloActivity()
    
    worker = Worker(
        client,
        task_queue="greeting-task-queue",
        workflows=[GreetingWorkflow],
        activities=[sayHelloActivity.execute],
    )
    
    await worker.run()