import time
import functools
from decorators import timer, logger, retry
import random


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()

        result = func(*args, **kwargs)

        end = time.time()
        print(f"[TIMER] {func.__name__} executed in {end - start:.6f} seconds")

        return result

    return wrapper


def logger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        print(f"[LOGGER] Calling {func.__name__}")
        print(f"[LOGGER] args={args}, kwargs={kwargs}")

        result = func(*args, **kwargs)

        print(f"[LOGGER] {func.__name__} returned {result}")

        return result

    return wrapper


def retry(max_attempts=3):
    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            attempts = 0

            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)

                except Exception as e:
                    attempts += 1
                    print(f"[RETRY] Attempt {attempts} failed: {e}")

                    if attempts == max_attempts:
                        print("[RETRY] Max attempts reached.")
                        raise

        return wrapper

    return decorator

@timer
@logger
def add(a, b):
    return a + b


@retry(max_attempts=3)
def unstable_function():
    if random.random() < 0.7:
        raise ValueError("Random failure!")
    return "Success"


print(add(5, 7))

print(unstable_function())