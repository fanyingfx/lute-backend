# type: ignore
import logging
import time
from functools import wraps

__all__ = (
    "sync_timed",
    "async_timed",
)


logging.basicConfig()
logger = logging.getLogger("time-logger")
logger.setLevel(logging.DEBUG)
# logger.setLevel(logging.)

ENABLE_DEBUG_LOGGING = False


def async_timed(func):
    """This decorator prints the execution time for the decorated function."""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        end = time.time()
        if ENABLE_DEBUG_LOGGING:
            logger.debug("%s ran in %.2fs", func.__name__, end - start)
        return result

    return wrapper


def sync_timed(func):
    """This decorator prints the execution time for the decorated function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        if ENABLE_DEBUG_LOGGING:
            logger.debug("%s ran in %.2fs", func.__name__, end - start)
        return result

    return wrapper
