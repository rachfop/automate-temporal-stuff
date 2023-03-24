import asyncio
from datetime import timedelta

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker

with workflow.unsafe.imports_passed_through():
    import pyautogui


@activity.defn
async def look_busy():
    pyautogui.moveRel(10, 0, 0.5)
    pyautogui.moveRel(-10, 0, 0.5)


@workflow.defn
class GreetingWorkflow:
    @workflow.run
    async def run(self):
        count = 0
        while True:
            if count != 1:
                print(f"Looked busy for {count} intervals.")
            else:
                print("Looked busy for 1 interval.")
            await workflow.execute_activity(
                look_busy,
                start_to_close_timeout=timedelta(seconds=10),
            )
            count += 1
            await asyncio.sleep(10)

        return "Done looking busy."


async def main():
    client = await Client.connect("localhost:7233")
    async with Worker(
        client,
        task_queue="look-busy-task-queue",
        workflows=[GreetingWorkflow],
        activities=[look_busy],
    ):
        print("Looking busy... press CTRL-C to quit.")
        result = await client.execute_workflow(
            GreetingWorkflow.run,
            id="look-busy-workflow-id",
            task_queue="look-busy-task-queue",
        )
        print(f"Result: {result}")


async def create_new_client_and_cancel():
    client = await Client.connect("localhost:7233")
    handle = client.get_workflow_handle("look-busy-workflow-id")
    await handle.cancel()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        asyncio.run(create_new_client_and_cancel())
        print("\nDone.")
