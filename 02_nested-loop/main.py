from functools import partial
import json

from fnutil import anyf, chain_where

# Find all items with chocolate batter and ppu >
# price_thresh_now, print their name.

#region Imperative

def imperative(data):
    price_threshold = data["price_thresh_now"]
    items = []
    
    candidate_items = data["items"]
    for item in candidate_items:
        is_chocolate = False
        
        for batter in item["batters"]:
            if (batter["id"] == "1002"):
                is_chocolate = True
                break
        
        if is_chocolate:
            items.append(item)
            
    for item in items:
        if item.get("ppu") > price_threshold:
            print(item["name"]) 

#endregion  

#region Functional 
  
def has_type_batter(batter_id, item):
    return anyf(lambda batter: batter_id == batter["id"], item["batters"])

def above_price_threshold(threshold, item):
    return item["ppu"] > threshold
 
def functional(data):
    price_threshold = data["price_thresh_now"]
    has_chocolate_batter = partial(has_type_batter, "1002")
    should_be_printed = chain_where(
        has_chocolate_batter,
        partial(above_price_threshold, price_threshold)
    )
    
    items = filter(should_be_printed, data["items"]) 
    names = list(map(lambda i: i["name"], items))
    
    for name in names:
        print(name)
    
#endregion

with open("data/bakery_inventory.json") as file:
    x = json.load(file)
    imperative(x)
    functional(x)
