import json
from functools import partial
from typing import Any, Dict, Iterable

def filter_item_above_threshold(threshold: float, item) -> bool:
    return item["ppu"] > threshold

def filter_item_type(type: str, item) -> bool:
    return item["type"] == type

def get_above_threshold_items(data: Dict[str, Any]) -> Iterable[Any]:
    price_threshold = data["price_thresh_now"]
    items = []
    is_above_threshold = partial(filter_item_above_threshold, price_threshold)

    for item in data["items"]:
        if is_above_threshold(item):
            items.append(item)

    return items

def get_items_of_type(data: Dict[str, Any], type: str) -> Iterable[Any]:
    items = []
    is_type = partial(filter_item_type, type)
    
    for item in data["items"]:
        if is_type(item):
            items.append(item)

    return items

with open("data/bakery_inventory.json") as file: 
    data = json.load(file)
    items = get_above_threshold_items(data)
    donuts = get_items_of_type(data, "donut")
    
    print("\nPrinting items above threshold")
    for item in items: 
        print("{0}: {1}".format(item["id"], item["name"]))
    
    print("\nPrinting donuts")
    for donut in donuts:
        print("{0}: {1}".format(donut["id"], donut["name"]))