import time
from functools import wraps
import logging

logger = logging.getLogger(__name__)

def retry(max_attempts: int = 3, delay_seconds: int = 2, on_failure=None) -> callable:
    """
    Retry decorator for test scenarios.
    Args:
        max_attempts (int): Number of retry attempts.
        delay_seconds (int): Delay between retries.
        on_failure (callable): Callback function to run on each failure (e.g., capture screenshot).
    Returns:
        callable: Decorator for retry logic.
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