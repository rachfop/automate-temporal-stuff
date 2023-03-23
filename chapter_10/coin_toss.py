import asyncio
from dataclasses import dataclass
from datetime import timedelta

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker
import random

"""Debug Coin Toss Program."""


# 0 is tails, 1 is heads


@dataclass
class CoinTossInput:
    guess: str
    toss: str


@activity.defn
async def coin_toss(input: CoinTossInput) -> str:
    if input.toss == input.guess:
        print("You won!")
    else:
        print("Nope. You are really bad at this game.")

    return input.guess


@workflow.defn
class CoinTossWorkflow:
    @workflow.run
    async def run(self, input: CoinTossInput) -> str:
        return await workflow.execute_activity(
            coin_toss,
            input,
            start_to_close_timeout=timedelta(seconds=10),
        )


async def main():
    client = await Client.connect("localhost:7233")
    async with Worker(
        client,
        task_queue="hello-activity-task-queue",
        workflows=[CoinTossWorkflow],
        activities=[coin_toss],
    ):
        guess = input("Guess the coin toss! Enter heads or tails: ")
        if guess != "heads" and guess != "tails":
            raise Exception("Guess must be heads or tails!")
        GUESS_CONVERTER = {0: "heads", 1: "tails"}
        toss = GUESS_CONVERTER[random.randint(0, 1)]
        guess_data = CoinTossInput(guess, toss)
        result = await client.execute_workflow(
            CoinTossWorkflow.run,
            guess_data,
            id="coin-toss",
            task_queue="hello-activity-task-queue",
        )
        print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
