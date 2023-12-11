#!/usr/bin/env/python3
import time
from functools import wraps
from contextlib import contextmanager

# https://www.learndatasci.com/solutions/python-timer/
# https://dev.to/kcdchennai/python-decorator-to-measure-execution-time-54hk

@contextmanager
def perf_context():
    """Performance timer for use as a context (with)"""
    t0 = time.perf_counter()
    try:
        yield
    finally:
        t1 = time.perf_counter()
        elapsed = t1 - t0
        print(f'{elapsed:0.4f}')

#
# Performance Decorator
# @perf_timer on function to be evaluated
#
def perf_timer(func):
    """Performance timer decorator"""
    total_time, runs = 0, 0

    @wraps(func)
    def _timer(*args, **kwargs):
        """Timer wrapper"""
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        t1 = time.perf_counter()
        elapsed = t1 - t0

        # bring variables into scope
        nonlocal total_time, runs
        runs += 1
        total_time += elapsed

        print(f"@perf_timer: {func.__name__} took {elapsed:0.4f} seconds")
        print(f"@perf_timer: The average run time is {(total_time / runs):0.4f} seconds\n")

        return result

    return _timer
