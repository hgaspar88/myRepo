import unittest
from unittest.mock import patch
from ratelimit.token_bucket import TokenBucket

class TestTokenBucket(unittest.TestCase):

    def setUp(self):
        # Use a mock clock to control time in tests
        self.mock_time = 0.0
        self.clock = lambda: self.mock_time

    def test_initialization(self):
        # Test valid initialization
        bucket = TokenBucket(capacity=10, refill_rate=1.0, clock=self.clock)
        self.assertEqual(bucket.capacity, 10)
        self.assertEqual(bucket.refill_rate, 1.0)
        self.assertEqual(bucket.tokens, 10)
        self.assertEqual(bucket.last_refill_time, 0.0)

        # Test invalid capacity
        with self.assertRaises(ValueError):
            TokenBucket(capacity=0, refill_rate=1.0, clock=self.clock)

        # Test invalid refill_rate
        with self.assertRaises(ValueError):
            TokenBucket(capacity=10, refill_rate=0.0, clock=self.clock)

    def test_allow_success(self):
        bucket = TokenBucket(capacity=10, refill_rate=1.0, clock=self.clock)
        result = bucket.allow(cost=1)
        self.assertTrue(result)
        self.assertEqual(bucket.tokens, 9)

    def test_allow_failure(self):
        bucket = TokenBucket(capacity=10, refill_rate=1.0, clock=self.clock)
        # Consume all tokens
        for _ in range(10):
            bucket.allow(cost=1)
        result = bucket.allow(cost=1)
        self.assertFalse(result)

    def test_allow_cost_exceeds_capacity(self):
        bucket = TokenBucket(capacity=10, refill_rate=1.0, clock=self.clock)
        with self.assertRaises(ValueError):
            bucket.allow(cost=11)

    def test_allow_cost_zero(self):
        bucket = TokenBucket(capacity=10, refill_rate=1.0, clock=self.clock)
        with self.assertRaises(ValueError):
            bucket.allow(cost=0)

    def test_allow_cost_negative(self):
        bucket = TokenBucket(capacity=10, refill_rate=1.0, clock=self.clock)
        with self.assertRaises(ValueError):
            bucket.allow(cost=-1)

    def test_allow_refill_after_time(self):
        bucket = TokenBucket(capacity=10, refill_rate=1.0, clock=self.clock)
        # Consume 10 tokens
        for _ in range(10):
            bucket.allow(cost=1)
        # After 1 second, refill one token
        self.mock_time = 1.0
        result = bucket.allow(cost=1)
        self.assertTrue(result)

    def test_allow_refill_after_multiple_seconds(self):
        bucket = TokenBucket(capacity=10, refill_rate=1.0, clock=self.clock)
        # Consume 10 tokens
        for _ in range(10):
            bucket.allow(cost=1)
        # After 10 seconds, refill 10 tokens
        self.mock_time = 10.0
        result = bucket.allow(cost=1)
        self.assertTrue(result)

    def test_retry_after_available(self):
        bucket = TokenBucket(capacity=10, refill_rate=1.0, clock=self.clock)
        result = bucket.retry_after(cost=1)
        self.assertEqual(result, 0.0)

    def test_retry_after_not_available(self):
        bucket = TokenBucket(capacity=10, refill_rate=1.0, clock=self.clock)
        # Consume all tokens
        for _ in range(10):
            bucket.allow(cost=1)
        # After 1 second, 1 token will be available
        self.mock_time = 1.0
        result = bucket.retry_after(cost=1)
        self.assertEqual(result, 0.0)

    def test_retry_after_not_available_immediately(self):
        bucket = TokenBucket(capacity=10, refill_rate=1.0, clock=self.clock)
        # Consume all tokens
        for _ in range(10):
            bucket.allow(cost=1)
        # No time passed yet
        result = bucket.retry_after(cost=1)
        self.assertEqual(result, 1.0)

    def test_retry_after_cost_exceeds_capacity(self):
        bucket = TokenBucket(capacity=10, refill_rate=1.0, clock=self.clock)
        with self.assertRaises(ValueError):
            bucket.retry_after(cost=11)

    def test_retry_after_cost_zero(self):
        bucket = TokenBucket(capacity=10, refill_rate=1.0, clock=self.clock)
        with self.assertRaises(ValueError):
            bucket.retry_after(cost=0)

    def test_retry_after_cost_negative(self):
        bucket = TokenBucket(capacity=10, refill_rate=1.0, clock=self.clock)
        with self.assertRaises(ValueError):
            bucket.retry_after(cost=-1)

    def test_refill_rate_half(self):
        bucket = TokenBucket(capacity=5, refill_rate=0.5, clock=self.clock)
        # Allow every 2 seconds
        self.mock_time = 0.0
        result = bucket.allow(cost=1)
        self.assertTrue(result)
        self.mock_time = 2.0
        result = bucket.allow(cost=1)
        self.assertTrue(result)

    def test_refill_rate_half_fails(self):
        bucket = TokenBucket(capacity=5, refill_rate=0.5, clock=self.clock)
        # Allow every 1 second
        self.mock_time = 0.0
        result = bucket.allow(cost=1)
        self.assertTrue(result)
        self.mock_time = 1.0
        result = bucket.allow(cost=1)
        self.assertFalse(result)

    def test_retry_after_after_failed_allow(self):
        bucket = TokenBucket(capacity=10, refill_rate=1.0, clock=self.clock)
        # Consume all tokens
        for _ in range(10):
            bucket.allow(cost=1)
        # After 1 second, 1 token will be available
        self.mock_time = 1.0
        result = bucket.retry_after(cost=1)
        self.assertEqual(result, 0.0)

    def test_retry_after_after_failed_allow_cost2(self):
        bucket = TokenBucket(capacity=10, refill_rate=1.0, clock=self.clock)
        # Consume all tokens
        for _ in range(10):
            bucket.allow(cost=1)
        # After 1 second, 1 token will be available
        self.mock_time = 1.0
        result = bucket.retry_after(cost=2)
        self.assertEqual(result, 1.0)

    def test_retry_after_after_failed_allow_cost2_immediate(self):
        bucket = TokenBucket(capacity=10, refill_rate=1.0, clock=self.clock)
        # Consume all tokens
        for _ in range(10):
            bucket.allow(cost=1)
        # No time passed yet
        result = bucket.retry_after(cost=2)
        self.assertEqual(result, 2.0)

    def test_allow_10_times_consecutive(self):
        bucket = TokenBucket(capacity=10, refill_rate=1.0, clock=self.clock)
        for _ in range(10):
            self.assertTrue(bucket.allow(cost=1))
        self.assertFalse(bucket.allow(cost=1))

    def test_allow_10_times_consecutive_and_wait_10_seconds(self):
        bucket = TokenBucket(capacity=10, refill_rate=1.0, clock=self.clock)
        for _ in range(10):
            self.assertTrue(bucket.allow(cost=1))
        self.mock_time = 10.0
        self.assertTrue(bucket.allow(cost=1))

    def test_allow_cost11(self):
        bucket = TokenBucket(capacity=10, refill_rate=1.0, clock=self.clock)
        with self.assertRaises(ValueError):
            bucket.allow(cost=11)