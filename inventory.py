"""Inventory management utilities with improved safety and style.

This module provides functions to manage a simple in-memory inventory,
load/save to JSON, and a small example `main`. Functions use
snake_case, validate inputs, avoid dangerous constructs (no eval,
no bare except), and use context managers for file I/O.
"""

import json
from datetime import datetime
from typing import Dict, List, Optional

stock_data: Dict[str, int] = {}


def add_item(item: str = "default", qty: int = 0, logs: Optional[List[str]] = None) -> None:
    """Add qty to an item. If logs is provided, append a timestamped message.

    Raises TypeError if item is not a string or qty cannot be converted to int.
    """
    if not item:
        return
    if not isinstance(item, str):
        raise TypeError("item must be a string")
    try:
        qty = int(qty)
    except (TypeError, ValueError):
        raise TypeError("qty must be an integer")
    stock_data[item] = stock_data.get(item, 0) + qty
    if logs is not None:
        logs.append(f"{datetime.now()}: Added {qty} of {item}")


def remove_item(item: str, qty: int) -> None:
    """Remove qty from an item; remove the item entirely if qty reduces to 0 or less.

    Silently returns if the item is not present.
    Raises TypeError if inputs are invalid.
    """
    if not isinstance(item, str):
        raise TypeError("item must be a string")
    try:
        qty = int(qty)
    except (TypeError, ValueError):
        raise TypeError("qty must be an integer")
    current = stock_data.get(item)
    if current is None:
        return
    new_qty = current - qty
    if new_qty > 0:
        stock_data[item] = new_qty
    else:
        del stock_data[item]


def get_qty(item: str) -> int:
    """Return the quantity for item or 0 if not present."""
    if not isinstance(item, str):
        raise TypeError("item must be a string")
    return stock_data.get(item, 0)


def load_data(file: str = "inventory.json") -> None:
    """Load inventory from a JSON file.

    If the file does not exist, the inventory is cleared. The file must
    contain a JSON object mapping item names to integer quantities.
    """
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError("inventory file must contain a JSON object")
        new_data: Dict[str, int] = {}
        for k, v in data.items():
            key = k if isinstance(k, str) else str(k)
            try:
                new_data[key] = int(v)
            except (TypeError, ValueError):
                raise ValueError(f"Invalid quantity for item {key}: {v}")
        stock_data.clear()
        stock_data.update(new_data)
    except FileNotFoundError:
        stock_data.clear()


def save_data(file: str = "inventory.json") -> None:
    """Save the inventory to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(stock_data, f, indent=2)


def print_data() -> None:
    """Print a human-readable report of current inventory."""
    print("Items Report")
    for name in sorted(stock_data):
        print(name, "->", stock_data[name])


def check_low_items(threshold: int = 5) -> List[str]:
    """Return a list of items whose quantity is below the given threshold.

    Raises TypeError if threshold is not an integer.
    """
    try:
        threshold = int(threshold)
    except (TypeError, ValueError):
        raise TypeError("threshold must be an integer")
    return [name for name, qty in stock_data.items() if qty < threshold]


def main() -> None:
    """Example usage of the inventory helpers."""
    logs: List[str] = []
    add_item("apple", 10, logs)
    add_item("banana", -2, logs)
    try:
        add_item(123, "ten", logs)
    except TypeError:
        logs.append(f"{datetime.now()}: Failed to add invalid item or qty")
    remove_item("apple", 3)
    remove_item("orange", 1)
    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())
    save_data()
    load_data()
    print_data()
    # Avoid unsafe eval usage; record an informational log message instead.
    logs.append(f"{datetime.now()}: eval avoided - using safe logging")


if __name__ == "__main__":
    main()
