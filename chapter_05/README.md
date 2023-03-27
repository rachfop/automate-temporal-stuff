# Chapter 05: Game Inventory

![Demo of the application](demo.gif)

This project demonstrates how to use Temporal to build a game inventory system. The inventory is represented as a list of InventoryItems, and we have two activities that can be performed on the inventory:

- `add_to_inventory`: takes an Inventory and a list of items to add, and returns an updated Inventory with the new items added.
- `display_inventory`: takes an Inventory and prints its contents and total number of items.

```python
poetry run python game_inventory.py
```

You should see an output similar to the following:

```bash
Inventory:
1 rope
6 torch
45 gold coin
1 dagger
12 arrow
3 map fragments
1 ruby
Total number of items : 68
```