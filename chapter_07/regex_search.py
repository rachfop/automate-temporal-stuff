import asyncio
from dataclasses import dataclass
from datetime import timedelta

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker

"""A Regex version of the Strip Function."""


@dataclass
class RegexSearchInput:
    text: str
    remove: str


@activity.defn
async def strip(input: RegexSearchInput) -> str:
    return input.text.replace(input.remove, "")


@workflow.defn
class StripWorkflow:
    @workflow.run
    async def run(self, input: RegexSearchInput) -> str:
        return await workflow.execute_activity(
            strip,
            input,
            start_to_close_timeout=timedelta(seconds=10),
        )


async def main():
    client = await Client.connect("localhost:7233")
    async with Worker(
        client,
        task_queue="hello-activity-task-queue",
        workflows=[StripWorkflow],
        activities=[strip],
    ):
        x = input("Enter the text you would like stripped here: ")
        y = (
            input(
                "Enter the character you want stripped here"
                " (Removes Space as Default): "
            )
            or " "
        )
        input_data = RegexSearchInput(x, y)
        result = await client.execute_workflow(
            StripWorkflow.run,
            input_data,
            id="regex-wf",
            task_queue="hello-activity-task-queue",
        )
        print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
