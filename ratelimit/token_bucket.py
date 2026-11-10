import time
from typing import Callable, Optional

class TokenBucket:
    """
    A token bucket rate limiter that enforces rate limits using a monotonic clock.

    The bucket refills tokens at a fixed rate, and each request consumes a cost of tokens.
    """

    def __init__(self, capacity: int, refill_rate: float, clock: Callable[[], float] = time.monotonic):
        """
        Initialize a token bucket with given capacity and refill rate.

        Args:
            capacity: The maximum number of tokens (must be > 0)
            refill_rate: The rate at which tokens are refilled per second (must be > 0)
            clock: A callable that returns monotonic time in seconds (default: time.monotonic)

        Raises:
            ValueError: If capacity <= 0 or refill_rate <= 0
        """
        if capacity <= 0:
            raise ValueError("capacity must be greater than 0")
        if refill_rate <= 0:
            raise ValueError("refill_rate must be greater than 0")

        self.capacity = capacity
        self.refill_rate = refill_rate
        self.clock = clock
        self.tokens: float = capacity
        self.last_refill_time: float = clock()

    def allow(self, cost: int) -> bool:
        """
        Attempt to consume `cost` tokens.

        Args:
            cost: The number of tokens to consume (must be > 0)

        Returns:
            True if enough tokens are available and consumed, False otherwise

        Raises:
            ValueError: If cost <= 0 or cost > capacity
        """
        if cost <= 0:
            raise ValueError("cost must be greater than 0")
        if cost > self.capacity:
            raise ValueError("cost must not exceed capacity")

        # Refill tokens based on elapsed time
        now = self.clock()
        elapsed = now - self.last_refill_time
        tokens_to_add = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill_time = now

        # Check if enough tokens are available
        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False

    def retry_after(self, cost: int) -> float:
        """
        Calculate how long to wait until `cost` tokens are available.

        Args:
            cost: The number of tokens to consume (must be > 0)

        Returns:
            0.0 if `allow(cost)` would return True, otherwise the time in seconds
            until one token becomes available

        Raises:
            ValueError: If cost <= 0 or cost > capacity
        """
        if cost <= 0:
            raise ValueError("cost must be greater than 0")
        if cost > self.capacity:
            raise ValueError("cost must not exceed capacity")

        # Refill tokens based on elapsed time
        now = self.clock()
        elapsed = now - self.last_refill_time
        tokens_to_add = elapsed * self.refill_rate
        available_tokens = min(self.capacity, self.tokens + tokens_to_add)

        if available_tokens >= cost:
            return 0.0

        # Compute time needed to refill enough tokens
        needed_tokens = cost - available_tokens
        time_to_wait = needed_tokens / self.refill_rate
        return time_to_wait