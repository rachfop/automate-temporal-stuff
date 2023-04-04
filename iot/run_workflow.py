import asyncio
from node_data import NodeMeasurement
from env_workflow import CO2EnvironmentWorkflow

from temporalio.client import Client


async def main():
    while True:
        client = await Client.connect("localhost:7233")
        result = await client.execute_workflow(
            CO2EnvironmentWorkflow.run,
            NodeMeasurement(
                co2="0",
                humidity="0",
                temperature="0",
            ),
            id="air-workflow-id",
            task_queue="air-task-queue",
        )
        print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
