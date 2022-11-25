import json
from typing import Any, Dict, Iterable

def get_above_threshold_items(data: Dict[str, Any]) -> Iterable[Any]:
    price_threshold = data["price_thresh_now"]
    items = []

    for item in data["items"]:
        if item["ppu"] > price_threshold:
            items.append(item)

    return items

def get_items_of_type(data: Dict[str, Any], type: str) -> Iterable[Any]:
    items = []
    
    for item in data["items"]:
        if item["type"] == type:
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