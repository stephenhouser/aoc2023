"""Performance wrapper functions

"""
import functools
import locale
import time

locale.setlocale(locale.LC_ALL, 'en_US')

TIMER_COUNTER = 0
TIMER_TOTAL = 0
TIMER_TIME = None
TIMER_START_TIME = None

def timer(func):
    """Wrap function and report on timing"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        global TIMER_COUNTER, TIMER_TOTAL, TIMER_START_TIME, TIMER_TIME

        TIMER_COUNTER += 1
        TIMER_TOTAL += 1
        value = func(*args, **kwargs)

        if not TIMER_START_TIME:
            TIMER_START_TIME = TIMER_TIME = time.perf_counter()

        now = time.perf_counter()
        if now - TIMER_TIME >= 1:
            processed_n = locale.format_string("%d", TIMER_COUNTER, grouping=True)
            total_n = locale.format_string("%d", TIMER_TOTAL, grouping=True)
            elapsed_time = int(now - TIMER_START_TIME)
            print(f"{processed_n:>15}, total={total_n} {elapsed_time}s")
            TIMER_TIME = time.perf_counter()
            TIMER_COUNTER = 0

        return value

    return wrapper_timer
