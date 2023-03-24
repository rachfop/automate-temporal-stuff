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
    lap_time: float = 0.0
    total_time: float = 0.0


@activity.defn
async def stopwatch(stop_watch_input: StopwatchInput):
    print("Started.")
    stop_watch_input.start_time = time.time()
    stop_watch_input.last_time = stop_watch_input.start_time
    stop_watch_input.lap_num = 1

    # Start tracking the lap times.

    while True:
        input()

        stop_watch_input.lap_time = round(time.time() - stop_watch_input.last_time, 2)
        stop_watch_input.total_time = round(
            time.time() - stop_watch_input.start_time, 2
        )

        lap = "lap # {} {} ({})".format(
            (str(stop_watch_input.lap_num) + ":").ljust(3),
            str(stop_watch_input.total_time).rjust(5),
            str(stop_watch_input.lap_time).rjust(6),
        )
        print(lap, end="")

        stop_watch_input.lap_num += 1
        stop_watch_input.last_time = time.time()  # Reset the last lap time.
        pyperclip.copy(lap)  # Copy latest lap to clipboard.


@workflow.defn
class StopWatchWorkflow:
    @workflow.run
    async def run(self, input: StopwatchInput) -> str:
        return await workflow.execute_local_activity(
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


async def create_new_client_and_cancel():
    client = await Client.connect("localhost:7233")
    handle = client.get_workflow_handle("stopwatch")
    await handle.cancel()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        asyncio.run(create_new_client_and_cancel())
        print("\nDone.")
