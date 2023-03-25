import asyncio
from dataclasses import dataclass
from datetime import timedelta

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker


@dataclass
class ListJoinerInput:
    list: list


@activity.defn
async def list_joiner(input: ListJoinerInput) -> str:
    activity.logger.info("Running activity with parameter %s" % input)
    count = 0
    joined = ""
    while count < len(input.list) - 2:
        joined += input.list[count] + ", "
        count += 1
    if len(input.list) > 2:
        joined += input.list[-2] + ", and "
    else:
        joined += input.list[-2] + " and "
    joined += input.list[-1] + "."
    return joined


@workflow.defn
class ListJoinerWorkflow:
    @workflow.run
    async def run(self, input_list: list) -> str:
        return await workflow.execute_activity(
            list_joiner,
            ListJoinerInput(input_list),
            start_to_close_timeout=timedelta(seconds=10),
        )


async def main():
    client = await Client.connect("localhost:7233")
    async with Worker(
        client,
        task_queue="list-joiner-task-queue",
        workflows=[ListJoinerWorkflow],
        activities=[list_joiner],
    ):
        result = await client.execute_workflow(
            ListJoinerWorkflow.run,
            ["apples", "oranges", "bananas"],
            id="list-joiner-workflow-id",
            task_queue="list-joiner-task-queue",
        )
        print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
