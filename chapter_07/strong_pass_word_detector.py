#!/usr/bin/env python3

import re
import asyncio
from dataclasses import dataclass
from datetime import timedelta
from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker


"""Program to Detect whether a Password is Strong or Not."""


@dataclass
class PasswordClipBoard:
    password: str


@activity.defn
async def pass_strength_checker(clipboard: PasswordClipBoard) -> str:
    pass_length_regex = re.compile(r".{8,}")  # >= 8 characters
    pass_upper_regex = re.compile(r"[A-Z]")  # Contains an upper case letter
    pass_lower_regex = re.compile(r"[a-z]")  # Contains a lower case letter
    pass_digit_regex = re.compile(r"[0-9]")  # Contains a digit
    """Check if a password is strong."""
    if pass_length_regex.search(clipboard.password) is None:
        return "Needs to be at least 8 characters long"
    if pass_upper_regex.search(clipboard.password) is None:
        return "Needs an upper case letter"
    if pass_lower_regex.search(clipboard.password) is None:
        return "Needs a lower case letter"
    if pass_digit_regex.search(clipboard.password) is None:
        return "Needs a digit"
    else:
        return True


@workflow.defn
class PasswordWorkflow:
    @workflow.run
    async def run(self, password: PasswordClipBoard) -> str:
        return await workflow.execute_activity(
            pass_strength_checker,
            password,
            start_to_close_timeout=timedelta(seconds=10),
        )


async def main():
    client = await Client.connect("localhost:7233")
    async with Worker(
        client,
        task_queue="password-task-queue",
        workflows=[PasswordWorkflow],
        activities=[pass_strength_checker],
    ):
        password = PasswordClipBoard(input("Enter a password to check its strength:"))

        # create PasswordClipBoard object
        result = await client.execute_workflow(
            PasswordWorkflow.run,
            password,
            id="password-workflow-id",
            task_queue="password-task-queue",
        )
        if result is True:
            print("That's a strong password. Remember to use it for one site only.")
        else:
            print("That's a weak password. I wouldn't recommend using it")
        print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
