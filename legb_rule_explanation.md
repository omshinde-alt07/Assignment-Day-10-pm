# Q1 --- Conceptual: LEGB Rule

## What is the LEGB Rule?

Python resolves variable names using the **LEGB rule**, which defines
the order in which Python searches for variables.

  Level   Meaning     Description
  ------- ----------- ----------------------------------------------------
  L       Local       Variables defined inside the current function
  E       Enclosing   Variables in outer (enclosing) functions
  G       Global      Variables defined at the module level
  B       Built-in    Python's built‑in names like `len`, `sum`, `print`

Python searches for variables in the order **Local → Enclosing → Global
→ Built‑in**.

------------------------------------------------------------------------

## Example

``` python
x = "global"

def outer():
    x = "enclosing"

    def inner():
        x = "local"
        print(x)

    inner()

outer()
```

### Output

    local

Explanation:

-   Python first checks the **local scope** inside `inner()`.
-   Since `x = "local"` exists there, it prints `"local"`.
-   It never checks enclosing or global scopes.

------------------------------------------------------------------------

## Scope Lookup Diagram

    Built‑in Scope
         ↑
    Global Scope (x = "global")
         ↑
    Enclosing Scope (x = "enclosing")
         ↑
    Local Scope (x = "local")

Python always searches **from the most local scope outward**.

------------------------------------------------------------------------

## Local vs Global Variable Example

``` python
x = 10

def func():
    x = 5
    print(x)

func()
print(x)
```

### Output

    5
    10

Explanation:

-   Inside the function, `x = 5` is a **local variable**.
-   Outside the function, `x = 10` remains unchanged.
-   The local variable **shadows** the global variable.

------------------------------------------------------------------------

## The `global` Keyword

The `global` keyword allows a function to **modify a global variable**.

Example:

``` python
x = 10

def func():
    global x
    x = 20

func()
print(x)
```

### Output

    20

Explanation:

-   Without `global`, Python would create a **new local variable**.
-   With `global`, it modifies the variable in the **global scope**.

------------------------------------------------------------------------

## Why `global` is Considered a Code Smell

Using `global` is discouraged in professional codebases because it can
lead to:

1.  Hidden side effects
2.  Harder debugging
3.  Poor modular design
4.  Functions that are not reusable

Example:

``` python
counter = 0

def increment():
    global counter
    counter += 1
```

This function modifies global state, which can cause unexpected behavior
in larger systems.

------------------------------------------------------------------------

## Better Alternatives

### 1. Pass Values as Parameters

``` python
def increment(counter):
    return counter + 1
```

------------------------------------------------------------------------

### 2. Use a Class (Encapsulation)

``` python
class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1
```

------------------------------------------------------------------------

### 3. Use Closures

``` python
def counter():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment
```

Closures allow functions to maintain state **without using global
variables**.

------------------------------------------------------------------------

## Summary

The **LEGB rule** determines how Python resolves variable names:

    Local → Enclosing → Global → Built‑in

Key points:

-   Local variables override outer scopes.
-   Global variables can be accessed but should rarely be modified.
-   The `global` keyword allows modification of global variables but is
    often avoided.
-   Better alternatives include **function parameters, classes, and
    closures**.
