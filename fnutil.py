from functools import partial, reduce
from operator import getitem
from typing import Any, Callable, Iterable

def identity(x):
    return x

def anyf(where: Callable[[Any], bool], xs: Iterable[Any]) -> bool:
    for x in xs:
        if where(x):
            return True
        
    return False

def chain_where(*where: Callable[[Any], bool]):
    def _chain(preds, item):
        for pred in preds:
            if not pred(item):
                return False
    
        return True
    
    return partial(_chain, where)

def compose(*funcs):
    def compose_fn(f, g):
        return lambda x : f(g(x))

    return reduce(compose_fn, funcs, identity)

def get(accessor, item):
    return getitem(item, accessor) 