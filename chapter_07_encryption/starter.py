import asyncio
import dataclasses

import temporalio.converter
from temporalio.client import Client

from codec import EncryptionCodec
from worker import PasswordWorkflow
from data_objects import PasswordClipBoard


async def main():
    # Connect client
    client = await Client.connect(
        "localhost:7233",
        data_converter=dataclasses.replace(
            temporalio.converter.default(), payload_codec=EncryptionCodec()
        ),
    )

    password = PasswordClipBoard(input("Enter a password to check its strength:"))
    result = await client.execute_workflow(
        PasswordWorkflow.run,
        password,
        id="encryption-workflow-id",
        task_queue="encryption-task-queue",
    )
    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
