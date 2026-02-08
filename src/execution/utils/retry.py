import time
from functools import wraps
import logging

logger = logging.getLogger(__name__)

def retry(max_attempts: int = 3, delay_seconds: int = 2, on_failure=None):
    """
    Retry decorator for test scenarios
    :param max_attempts: Number of retry attempts
    :param delay_seconds: Delay between retries
    :param on_failure: Callback function to run on each failure (e.g., capture screenshot)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"Attempt {attempt} failed: {e}")
                    if on_failure:
                        on_failure(*args, **kwargs)
                    if attempt == max_attempts:
                        logger.error(f"💥 All {max_attempts} attempts failed for {func.__name__}")
                        raise
                    time.sleep(delay_seconds)
            return None
        return wrapper
    return decorator