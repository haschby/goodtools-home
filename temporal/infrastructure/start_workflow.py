import asyncio
from temporalio.client import Client
from application.workflows.greeting import GreetingWorkflow, GreetingWorkflowProps
from uuid import uuid4

async def start_workflow() -> None:
    client = await Client.connect("localhost:7233", namespace="default")
    
    workflow = await client.execute_workflow(
        GreetingWorkflow.run,
        GreetingWorkflowProps(name="Engineer"),
        id=f"GC-45090-TBD",
        task_queue="greeting-task-queue",
    )
    
    
    print(workflow)


asyncio.run(start_workflow())