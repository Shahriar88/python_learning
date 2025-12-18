# -*- coding: utf-8 -*-
"""
Created on Wed Dec 17 15:14:00 2025
@author: kec994
"""

import time
import functools


# 1) Timer decorator: prints elapsed time, returns original result
def timer(func):
    """Decorator that prints the run time of a function and returns the original result."""
    @functools.wraps(func)  # keeps func.__name__ and docstring
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start

        h, rem = divmod(elapsed, 3600)
        m, s = divmod(rem, 60)
        print(f"[TIMER] {func.__name__} finished in {int(h):02d}:{int(m):02d}:{s:05.2f} (hh:mm:ss)")

        return result
    return wrapper


@timer
def demo_single_return():
    a = 1
    print("Update your function")
    return a


@timer
def demo_multiple_return():
    a = 1
    b = 2
    return a, b


x = demo_single_return()          # x is 1
a, b = demo_multiple_return()     # a=1, b=2


# 2) Timer decorator: prints elapsed time AND returns elapsed
def timer_with_elapsed(func):
    """Decorator that returns (result, elapsed_seconds)."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start

        h, rem = divmod(elapsed, 3600)
        m, s = divmod(rem, 60)
        print(f"[TIMER] {func.__name__} finished in {int(h):02d}:{int(m):02d}:{s:05.2f} (hh:mm:ss)")

        return result, elapsed
    return wrapper


@timer_with_elapsed
def demo_single_return_with_elapsed():
    a = 1
    print("Update your function")
    return a


@timer_with_elapsed
def demo_multiple_return_with_elapsed():
    a = 1
    b = 2
    return a, b


x, elapsed = demo_single_return_with_elapsed()
(a, b), elapsed2 = demo_multiple_return_with_elapsed()

print("elapsed seconds =", elapsed)
print("a, b =", a, b, "elapsed2 =", elapsed2)








def timer_with_state(func):
    """
    Decorator that:
    - prints elapsed time
    - returns the original function result unchanged
    - stores timing in func.last_elapsed and func.last_elapsed_str
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start

        h, rem = divmod(elapsed, 3600)
        m, s = divmod(rem, 60)

        wrapper.last_elapsed = elapsed
        wrapper.last_elapsed_str = f"{int(h):02d}:{int(m):02d}:{s:05.2f} (hh:mm:ss)"

        print(f"[TIMER] {func.__name__} finished in {wrapper.last_elapsed_str}")
        return result

    wrapper.last_elapsed = None
    wrapper.last_elapsed_str = None
    return wrapper




@timer_with_state
def demo_single():
    time.sleep(0.2)
    return 42

x = demo_single()
print("x =", x)
print("elapsed seconds =", demo_single.last_elapsed)
print("elapsed string  =", demo_single.last_elapsed_str)

