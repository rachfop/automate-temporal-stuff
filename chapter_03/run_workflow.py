import asyncio

from temporalio.client import Client

from your_workflows import CollatzWorkflow


async def main():
    client = await Client.connect("localhost:7233")
    number = int(input("Choose any integer greater than 1: "))

    await client.execute_workflow(
        CollatzWorkflow.run,
        args=(number,),
        id="collatz-wf",
        task_queue="collatz-task-queue",
    )


if __name__ == "__main__":
    asyncio.run(main())
