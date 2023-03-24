import asyncio
import dataclasses

import temporalio.converter
from temporalio import workflow
from temporalio.client import Client
from temporalio.worker import Worker

from codec import EncryptionCodec
from password_strength_activity import pass_strength_checker
from data_objects import PasswordClipBoard
from datetime import timedelta


@workflow.defn
class PasswordWorkflow:
    @workflow.run
    async def run(self, password: PasswordClipBoard) -> str:
        return await workflow.execute_activity(
            pass_strength_checker,
            password,
            start_to_close_timeout=timedelta(seconds=10),
        )


interrupt_event = asyncio.Event()


async def main():
    # Connect client
    client = await Client.connect(
        "localhost:7233",
        # Use the default converter, but change the codec
        data_converter=dataclasses.replace(
            temporalio.converter.default(), payload_codec=EncryptionCodec()
        ),
    )

    # Run a worker for the workflow
    async with Worker(
        client,
        task_queue="encryption-task-queue",
        workflows=[PasswordWorkflow],
        activities=[pass_strength_checker],
    ):
        # Wait until interrupted
        print("Worker started, ctrl+c to exit")
        await interrupt_event.wait()
        print("Shutting down")


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        interrupt_event.set()
        loop.run_until_complete(loop.shutdown_asyncgens())
