# 01: Filtering an Iterable
This is the first is a (probably) series of writings on functional programming 
in Python. The intended audience of these posts is anyone who has basic
programming knowledge. Python experience helps but is not necessary.

Every post has an associated git branch, which you can use to follow along.

## An important note
It is first important to address a common concern regarding functional 
programming. Students learning functional programming have probably come across
this statement (or similar).

> All told, a monad in X is just a monoid in the category of endofunctors of X,
with product × replaced by composition of endofunctors and unit set by the
identity endofunctor. Mac Lane, Saunders. "Monads and Algebra." _Categories for
the Working Mathematician_, p. 138.

Way to muddy the waters. To understand how to use functional programming in
context of writing business software is not the same as understanding monoids, 
endofunctors, lambda calculus, and the like. I will not be using mathematical
terminology in these posts, because it is frankly not necessary.

## A simple example
> _Data_: [bakery_inventory.json](../data/bakery_inventory.json)<br>
_Code_: [Python code](../01_simple-example/main.py)<br>
_Branch_: `post/01-simple-example`<br>
_Requirement_: I need to know all items with a PPU (price per unit) greater
than the current price threshold.

The imperative approach is quite simple. The current price threshold is stored
in `price_thresh_now: float`, and items in `items: list`.

```py
def get_above_threshold_items(data: Dict[str, Any]) -> Iterable[Any]:
    price_threshold = data["price_thresh_now"]
    items = []

    for item in data["items"]:
        if item["ppu"] > price_threshold:
            items.append(item)

    return items
```

This function stores the current price threshold and the list of items to return 
in variables. A simple combination of a `for` loop and `if` finds items meeting 
the criteria, returning the list when done. 

Now we get a new requirement. 

> _Requirement_: I need to know all items that are a certain type. 

Type is a property `type: string` on each item. Another function is required
here. 

```py
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
def filter_item_type(type: str, item) -> bool:
    return item["type"] == type
```

Similarly, a function can be defined that `get_above_threshold_items` uses to
filter. 

```py
def filter_item_above_threshold(threshold: float, item) -> bool:
    return item["ppu"] > threshold
```

Now the definitions of our business logic can be changed. 

```py
def get_above_threshold_items(data: Dict[str, Any]) -> Iterable[Any]:
    price_threshold = data["price_thresh_now"]
    items = []

    for item in data["items"]:
        if filter_item_above_threshold(price_threshold, item):
            items.append(item)

    return items

def get_items_of_type(data: Dict[str, Any], type: str) -> Iterable[Any]:
    items = []
    
    for item in data["items"]:
        if filter_item_type(type, item):
            items.append(item)

    return items
```

I'll readily admit that these aren't naturally clearer to read. There is more 
code than before. Did this change actually simplify anything? Maybe there is a
better hammer in the toolbox.

### Python builtin: `filter()`

_Doc_: [builtins filter()](https://docs.python.org/3/library/functions.html#filter)

> Construct an iterator from those elements of iterable for which function returns
> true. iterable may be either a sequence, a container which supports iteration,
> or an iterator. If function is None, the identity function is assumed, that is,
> all elements of iterable that are false are removed.
> 
> Note that filter(function, iterable) is equivalent to the generator expression
> (item for item in iterable if function(item)) if function is not None and (item
> for item in iterable if item) if function is None.

Let us rephrase. 

> **`filter(function, iterable)`**
>
> Given a function and iterable, yield every item where `function(item) == True`.
>
> If `function == None`, then every item is yielded. 
>
> * arg `function: Callable[[Any], bool]`:
>       A function that takes one argument and returns `bool`. Used to 
>       determine if an item should be yielded.
> * arg `iterable: Iterable[Any]`:
>       Any object that can be used in a for loop, e.g. `for item in iterable`.

For example, to get a list of all odd numbers. 

```py
def is_odd(x):
    return x % 1 == 1

odd_numbers = filter(is_odd, range(100))
```

How does this apply to the functions written for filtering bakery items? Those
functions take two arguments, but the function passed to `filter()` takes one. 

### `functools.partial()`

_Doc_: [`functools.partial()`](https://docs.python.org/3/library/functools.html#functools.partial)

Basically, we can use `partial()` to create a function with argument already 
passed in. For example, using the `filter_item_above_threshold()` we wrote
before: 

```py
def get_above_threshold_items(data: Dict[str, Any]) -> Iterable[Any]:
    price_threshold = data["price_thresh_now"]
    items = []
    is_above_threshold = partial(filter_item_above_threshold, price_threshold)

    for item in data["items"]:
        if is_above_threshold(item):
            items.append(item)

    return items
```

Now we have the filter for the price in a function that takes one argument. 
It's exactly what we need to use `filter()`.

### Rewrite with filter and partial
With `filter()`, `get_above_threshold_items()` can be rewritten as: 

```py
def get_above_threshold_items(data: Dict[str, Any]) -> Iterable[Any]:
    price_threshold = data["price_thresh_now"]

    # Create our price filter
    is_above_threshold = partial(filter_item_above_threshold, price_threshold)

    # Just return filter; it is iterable
    return filter(is_above_threshold, data["items"])
```

Instead of expressing our business logic in terms of iterating through loops and
using `if` to conditionally execute code, we are programming in terms of our
business, with the help of some utility functions. 

Let's compare to the original. 

```py
def get_above_threshold_items(data: Dict[str, Any]) -> Iterable[Any]:
    price_threshold = data["price_thresh_now"]
    items = []

    for item in data["items"]:
        if item["ppu"] > price_threshold:
            items.append(item)

    return items
```

## Final Thoughts
Using `partial()` and `filter()`, we have been able to rewrite an imperative
implementation of business logic with a functional one. 

This first post is less about simplifying and more about showing a different 
way of expressing program logic. Later examples will build on these concepts to
tackle more complex requirements. 
