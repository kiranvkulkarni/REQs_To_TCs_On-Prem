import time
from functools import wraps
import logging

logger = logging.getLogger(__name__)

def retry(max_attempts: int = 3, delay_seconds: int = 2):
    """
    Retry decorator for functions
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"Attempt {attempt} failed: {e}")
                    if attempt == max_attempts:
                        logger.error(f"💥 All {max_attempts} attempts failed for {func.__name__}")
                        raise
                    time.sleep(delay_seconds)
            return None
        return wrapper
    return decorator