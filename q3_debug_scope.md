# Q3 --- Debug / Analyze

## Original Code

``` python
total = 0

def add_to_cart(item, cart=[]):      # Bug 1: mutable default
    cart.append(item)
    total = total + len(cart)        # Bug 2: scope issue
    return cart

print(add_to_cart('apple'))
print(add_to_cart('banana'))
```

This code contains **two bugs**:

1.  Mutable default argument
2.  Scope issue

------------------------------------------------------------------------

# Bug 1 --- Mutable Default Argument

Problem:

    cart=[]

Default arguments in Python are evaluated **once when the function is
defined**, not each time it is called.

Therefore the same list is reused across calls.

### What Happens

    add_to_cart('apple')  -> ['apple']
    add_to_cart('banana') -> ['apple','banana']

But we expected:

    ['banana']

------------------------------------------------------------------------

# Bug 2 --- Scope Issue

This line causes an error:

``` python
total = total + len(cart)
```

Python assumes `total` is a **local variable** because it is assigned
inside the function.

But it is referenced before assignment.

This causes:

    UnboundLocalError

------------------------------------------------------------------------

# Fixing Both Bugs

## Fix 1: Avoid Mutable Defaults

Use `None` instead.

## Fix 2: Handle Global Variable Correctly

Example fix:

``` python
total = 0

def add_to_cart(item, cart=None):
    global total

    if cart is None:
        cart = []

    cart.append(item)
    total += len(cart)

    return cart
```

------------------------------------------------------------------------

# Better Design (Avoid Global State)

A cleaner solution avoids modifying global variables entirely.

``` python
def add_to_cart(item, cart=None):
    if cart is None:
        cart = []

    cart.append(item)
    return cart
```

------------------------------------------------------------------------

# Correct Output

    print(add_to_cart('apple'))
    ['apple']

    print(add_to_cart('banana'))
    ['banana']

Each function call now creates a **new list**.

------------------------------------------------------------------------

# Key Lessons

1.  Never use **mutable objects as default arguments**
2.  Understand **Python scope rules**
3.  Avoid **global state when possible**
