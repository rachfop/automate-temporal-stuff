from temporalio.client import Client
from temporalio.worker import Worker
from co2_activity import get_latest_measurements, send_message

from run_workflow import CO2EnvironmentWorkflow
import asyncio


async def main():
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="air-task-queue",
        workflows=[CO2EnvironmentWorkflow],
        activities=[get_latest_measurements, send_message],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
