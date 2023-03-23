import asyncio
from dataclasses import dataclass
from datetime import timedelta

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker


@dataclass
class CharacterGridInput:
    grid: list


@activity.defn
async def print_grid(input: CharacterGridInput) -> None:
    for i in range(len(input.grid[0])):
        for j in range(len(input.grid)):
            print(input.grid[j][i], end="")
        print()


@workflow.defn
class CharacterGridWorkflow:
    @workflow.run
    async def run(self, grid: list) -> None:
        await workflow.execute_activity(
            print_grid,
            CharacterGridInput(grid),
            start_to_close_timeout=timedelta(seconds=10),
        )


async def main():
    client = await Client.connect("localhost:7233")
    async with Worker(
        client,
        task_queue="character-grid-task-queue",
        workflows=[CharacterGridWorkflow],
        activities=[print_grid],
    ):
        await client.execute_workflow(
            CharacterGridWorkflow.run,
            [
                [".", ".", ".", ".", ".", "."],
                [".", "O", "O", ".", ".", "."],
                ["O", "O", "O", "O", ".", "."],
                ["O", "O", "O", "O", "O", "."],
                [".", "O", "O", "O", "O", "O"],
                ["O", "O", "O", "O", "O", "."],
                ["O", "O", "O", "O", ".", "."],
                [".", "O", "O", ".", ".", "."],
                [".", ".", ".", ".", ".", "."],
            ],
            id="character-grid-workflow-id",
            task_queue="character-grid-task-queue",
        )


if __name__ == "__main__":
    asyncio.run(main())
