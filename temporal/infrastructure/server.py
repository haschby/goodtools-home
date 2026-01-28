import asyncio
from .worker.worker import start_worker

async def bootstrap() -> None:
    await start_worker()

asyncio.run(bootstrap())
    