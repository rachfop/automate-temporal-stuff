from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker
import asyncio
from dataclasses import dataclass
from datetime import timedelta
from typing import List


@dataclass
class Table:
    items: List[List[str]]


@activity.defn
async def print_table(table: Table) -> str:
    """Return a formatted, properly aligned table version of a list as a string."""
    # Create list with zeroes equal to the length of input list
    col_widths = [0] * len(table.items)

    # Finds longest word in each sublists and sets col_width[x] to value
    count = 0
    while count < len(table.items):
        for item in table.items[count]:
            if len(item) > col_widths[count]:
                col_widths[count] = len(item)
        count += 1

    # Iterates over lists taking nth element from each
    # and printing it with the other nth subitems
    # right aligned according to the corresponding col_width value
    table_str = ""
    for word in range(len(table.items[0])):
        for item in range(len(table.items)):
            table_str += table.items[item][word].rjust(col_widths[item]) + " "
        table_str += "\n"

    return table_str


@workflow.defn
class PrintTableWorkflow:
    @workflow.run
    async def run(self, table_data: Table) -> str:
        return await workflow.execute_activity(
            print_table,
            table_data,
            start_to_close_timeout=timedelta(seconds=10),
        )


async def main():
    client = await Client.connect("localhost:7233")
    async with Worker(
        client,
        task_queue="table-task-queue",
        workflows=[PrintTableWorkflow],
        activities=[print_table],
    ):
        result = await client.execute_workflow(
            PrintTableWorkflow.run,
            Table(
                [
                    ["apples", "oranges", "cherries", "banana"],
                    ["Alice", "Bob", "Carol", "David"],
                    ["dogs", "cats", "moose", "goose"],
                ]
            ),
            id="print-table-wf",
            task_queue="table-task-queue",
        )
        print(f"{result}")


if __name__ == "__main__":
    asyncio.run(main())
