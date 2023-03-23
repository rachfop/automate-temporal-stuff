import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from collatz_activity import collatz, graph
from your_workflows import CollatzWorkflow


async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="collatz-task-queue",
        workflows=[CollatzWorkflow],
        activities=[collatz, graph],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
