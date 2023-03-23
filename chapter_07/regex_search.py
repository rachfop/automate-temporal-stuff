import asyncio
from dataclasses import dataclass
from datetime import timedelta
import re

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker

#!/usr/bin/env python3

"""A Regex version of the Strip Function."""


@dataclass
class RegexSearchInput:
    text: str
    remove: str


@activity.defn
async def strip(input: RegexSearchInput) -> str:
    """Perform string.strip-like functions but using regexes."""
    # Removes whitespace from either end of the string
    if input.remove == "":
        space_regex = re.compile(r"^(\s*)(\S*)(\s)*$")
        trimmed = space_regex.search(input.text)
        return trimmed.group(2)

    # Removes character inputted as 2nd argument from ends of string
    else:
        remove_start = re.compile(r"^([%s]+)" % input.remove)
        remove_end = re.compile(r"([%s]+)$" % input.remove)
        start = remove_start.search(input.text)
        end = remove_end.search(input.text)
        # Allows function to strip even if only one side has remove characters
        try:
            return input.text[len(start.group()) : len(input.text) - len(end.group())]
        except AttributeError:
            error_avoid = input.remove + input.text + input.remove
            regex_search_input = RegexSearchInput(text=error_avoid, remove=input.remove)
            return await strip(regex_search_input)


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
