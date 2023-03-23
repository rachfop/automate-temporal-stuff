import asyncio
from dataclasses import dataclass
from datetime import timedelta
from typing import List
from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker


@dataclass
class InventoryItem:
    name: str
    quantity: int


@dataclass
class Inventory:
    items: List[InventoryItem]


@activity.defn
async def display_inventory(inventory: Inventory):
    """Print contents and total number of items in inventory."""
    print("Inventory:")
    item_total = 0
    for item in inventory.items:
        print(str(item.quantity) + " " + item.name)
        item_total += item.quantity
    print("Total number of items : " + str(item_total))


@workflow.defn
class GameInventoryWorkflow:
    @workflow.run
    async def run(self, input: List[str]) -> None:
        inventory = Inventory(
            [
                InventoryItem("rope", 1),
                InventoryItem("torch", 6),
                InventoryItem("gold coin", 42),
                InventoryItem("dagger", 1),
                InventoryItem("arrow", 12),
                InventoryItem("map fragments", 3),
            ]
        )
        for loot in input:
            inventory = await workflow.execute_activity(
                add_to_inventory,
                AddToInventoryInput(inventory, [loot]),
                start_to_close_timeout=timedelta(seconds=10),
            )
        return await display_inventory(inventory)


@dataclass
class AddToInventoryInput:
    inventory: Inventory
    added_items: List[str]


@activity.defn
async def add_to_inventory(input: AddToInventoryInput) -> Inventory:
    """Combine a list of loot with an inventory."""
    inventory_dict = {item.name: item.quantity for item in input.inventory.items}
    for loot in input.added_items:
        inventory_dict.setdefault(loot, 0)
        inventory_dict[loot] += 1
    inventory_items = [
        InventoryItem(name, quantity) for name, quantity in inventory_dict.items()
    ]
    return Inventory(items=inventory_items)


async def main():
    client = await Client.connect("localhost:7233")
    async with Worker(
        client,
        task_queue="game-inventory-task-queue",
        workflows=[GameInventoryWorkflow],
        activities=[display_inventory, add_to_inventory],
    ):
        await client.execute_workflow(
            GameInventoryWorkflow.run,
            ["gold coin", "dagger", "gold coin", "gold coin", "ruby"],
            id="hello-activity-workflow-id",
            task_queue="game-inventory-task-queue",
        )


if __name__ == "__main__":
    asyncio.run(main())
