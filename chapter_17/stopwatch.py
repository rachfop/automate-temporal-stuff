#!/usr/bin/env python3

"""A stopwatch program with a prettier output and pyperclip functionality."""

import time
import pyperclip

# Display the programs instructions.


import asyncio
from dataclasses import dataclass
from datetime import timedelta

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker


@dataclass
class StopwatchInput:
    start_time: float
    last_time: float
    lap_num: int


@activity.defn
async def stopwatch(input: StopwatchInput):
    print("Started.")
    input.start_time = time.time()
    input.last_time = input.start_time
    input.lap_num = 1

    # Start tracking the lap times.
    try:
        while True:
            input = StopwatchInput(
                start_time=input.start_time,
                last_time=input.last_time,
                lap_num=input.lap_num,
            )
            input.lap_time = round(time.time() - input.last_time, 2)
            input.total_time = round(time.time() - input.start_time, 2)

            lap = "lap # {} {} ({})".format(
                (str(input.lap_num) + ":").ljust(3),
                str(input.total_time).rjust(5),
                str(input.lap_time).rjust(6),
            )
            print(lap, end="")

            input.lap_num += 1
            input.last_time = time.time()  # Reset the last lap time.
            pyperclip.copy(lap)  # Copy latest lap to clipboard.
    except KeyboardInterrupt:
        print("\nDone.")


@workflow.defn
class StopWatchWorkflow:
    @workflow.run
    async def run(self, input: StopwatchInput) -> str:
        return await workflow.execute_activity(
            stopwatch,
            input,
            start_to_close_timeout=timedelta(seconds=10),
        )


async def main():
    client = await Client.connect("localhost:7233")
    async with Worker(
        client,
        task_queue="stopwatch-task-queue",
        workflows=[StopWatchWorkflow],
        activities=[stopwatch],
    ):
        print(
            'Press ENTER to begin. Afterwards, press ENTER to "click" the stopwatch.'
            "Press Ctrl-c to quit."
        )

        input_obj = StopwatchInput(start_time=0.0, last_time=0.0, lap_num=0)
        result = await client.execute_workflow(
            StopWatchWorkflow.run,
            input_obj,
            id="stopwatch",
            task_queue="stopwatch-task-queue",
        )
        print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
