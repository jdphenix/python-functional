# 01: Filtering an Iterable
This is the first is a (probably) series of writings on functional programming 
in Python. The intended audience of these posts is anyone who has basic
programming knowledge. Python experience helps but is not necessary.

Every post has an associated git branch, which you can use to follow along.

## An important note
It is first important to address a common concern regarding functional 
programming. Students learning functional programming have probably come across
this statement. 

> All told, a monad in X is just a monoid in the category of endofunctors of X,
with product × replaced by composition of endofunctors and unit set by the
identity endofunctor. Mac Lane, Saunders. "Monads and Algebra." _Categories for
the Working Mathematician_, p. 138.

Way to muddle the waters. To understand how to use functional programming in
context of writing business software is not the same as understanding monoids, 
endofunctos, lambda calculus, and the like. I will not be using mathematical
terminology in these posts, because it is frankly not necessary.

## A simple example
> _Data_: [bakery_inventory.json](../data/bakery_inventory.json)<br>
_Code_: [Python code](../01_simple-example/imperative.py)<br>
_Branch_: `post/01-simple-example`<br>
_Requirement_: I need to know all items with a PPU (price per unit) greater
than the current price threshold.

The imperative approach is quite simple. The current price threshold is stored
in `price_thresh_now: float`, and items in `items: list`.

```py
from typing import Any, Dict, Iterable

def get_above_threshold_items(data: Dict[str, Any]) -> Iterable[Any]:
    price_threshold = data["price_thresh_now"]
    items = []

    for item in data["items"]:
        if item["ppu"] > price_threshold:
            items.append(item)

    return items
```

This function stores the current price threshold and the list of items to return in
variables. A simple combination of a `for` loop and `if` finds items meeting the
criteria, returning the list when done. 

Now we get a new requirement. 

> _Requirement_: I need to know all items that are a certain type. 

Type is a property `type: string` on each item. Another function is required
here. 

```py
from typing import Any, Dict, Iterable

def get_items_of_type(data: Dict[str, Any], type: str) -> Iterable[Any]:
    items = []
    
    for item in data["items"]:
        if item["type"] == type:
            items.append(item)

    return items
```

This function is similar to `get_above_threshold_items`, however it accepts a
second parameter to filter the items' types. 

## Introducing functional programming
Review `get_above_threshold_items` and `get_items_of_type`. Note that they
perform very similar functions, and in much the same manner. Let's see how we
can abstract out common functionality. 

Consider `get_items_of_type`, and note that the `if` clause is filtering out 
items that don't pass it. We can define a function that does this for one item.

```py
def filter_item_type(item, type: str) -> bool:
    return item["type"] == type
```