import os
import re
import asyncio
from dataclasses import dataclass
from datetime import timedelta

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker


@dataclass
class MadLibInput:
    file_name: str
    match: str


@activity.defn
async def compose_greeting(madlib: MadLibInput) -> str:
    lib = open("{0}/chapter_08/{1}.txt".format(os.getcwd(), madlib.file_name))

    string = lib.read()
    for madlib.match in re.findall(
        r"\bVERB\b|\bNOUN\b|\bADVERB\b|\bADJECTIVE\b", string
    ):
        sub = input(f"Enter a {madlib.match}: ")
        string = string.replace(madlib.match, sub, 1)
    return string


@workflow.defn
class GreetingWorkflow:
    @workflow.run
    async def run(self, madlib_input: MadLibInput) -> str:
        return await workflow.execute_activity(
            compose_greeting,
            madlib_input,
            start_to_close_timeout=timedelta(seconds=60),
        )


async def main():
    client = await Client.connect("localhost:7233")
    async with Worker(
        client,
        task_queue="madlib-task-queue",
        workflows=[GreetingWorkflow],
        activities=[compose_greeting],
    ):
        madlib_input = MadLibInput("madlib", "")
        result = await client.execute_workflow(
            GreetingWorkflow.run,
            madlib_input,
            id="madlib-workflow-id",
            task_queue="madlib-task-queue",
        )
        print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
