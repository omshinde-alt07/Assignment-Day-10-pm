# Q2 --- Coding: Memoization Decorator

## Problem

Write a function `memoize(func)` that caches results of expensive
function calls. When called with the same arguments, it should return
the cached result instead of recomputing.

Example usage:

``` python
@memoize
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(50))
```

Without memoization, this would take a very long time because the same
Fibonacci values are recomputed many times.

------------------------------------------------------------------------

## Memoization Decorator Implementation

``` python
from functools import wraps

def memoize(func):
    cache = {}

    @wraps(func)
    def wrapper(*args):
        if args in cache:
            return cache[args]

        result = func(*args)
        cache[args] = result
        return result

    return wrapper
```

------------------------------------------------------------------------

## Example: Fibonacci with Memoization

``` python
@memoize
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(50))
```

------------------------------------------------------------------------

## Why Memoization Works

Without memoization, the recursion tree looks like this:

    fib(5)
    ├── fib(4)
    │   ├── fib(3)
    │   ├── fib(2)
    ├── fib(3)

Many values like `fib(3)` are calculated multiple times.

With memoization:

    fib(5)
    fib(4)
    fib(3)
    fib(2)
    fib(1)
    fib(0)

Each value is calculated **once**, then stored in the cache.

------------------------------------------------------------------------

## Time Complexity

  Approach              Complexity
  --------------------- ------------
  Without memoization   O(2\^n)
  With memoization      O(n)

------------------------------------------------------------------------

## Key Concepts Used

-   **Decorator pattern**
-   **Closures**
-   `*args` to support any function signature
-   `functools.wraps` to preserve function metadata
-   **Dictionary caching**
