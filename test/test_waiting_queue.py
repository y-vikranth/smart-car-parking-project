import unittest
from core.waiting_queue import WaitingQueue
from core.vehicle import Vehicle
import time

class TestWaitingQueue(unittest.TestCase):

    def setUp(self):
        self.queue = WaitingQueue(max_size=3)
        self.vehicle1 = Vehicle("1234")
        self.vehicle2 = Vehicle("5678")
        self.vehicle3 = Vehicle("9101")
        self.vehicle4 = Vehicle("1122")  # For testing overflow

    def test_enqueue_success(self):
        result = self.queue.enqueue(self.vehicle1)
        self.assertTrue(result)
        self.assertEqual(self.queue.size(), 1)
        self.assertEqual(self.queue.peek().license_plate, "1234")
        self.assertIsNotNone(self.vehicle1.queue_entry_time)

    def test_enqueue_failure_when_full(self):
        self.queue.enqueue(self.vehicle1)
        self.queue.enqueue(self.vehicle2)
        self.queue.enqueue(self.vehicle3)
        result = self.queue.enqueue(self.vehicle4)  # Should fail
        self.assertFalse(result)
        self.assertEqual(self.queue.size(), 3)

    def test_dequeue_success(self):
        self.queue.enqueue(self.vehicle1)
        self.queue.enqueue(self.vehicle2)
        dequeued = self.queue.dequeue()
        self.assertEqual(dequeued.license_plate, "1234")
        self.assertEqual(self.queue.size(), 1)
        self.assertIsNotNone(dequeued.queue_exit_time)

    def test_dequeue_when_empty(self):
        result = self.queue.dequeue()
        self.assertIsNone(result)

    def test_peek(self):
        self.queue.enqueue(self.vehicle1)
        peeked = self.queue.peek()
        self.assertEqual(peeked.license_plate, "1234")
        self.assertEqual(self.queue.size(), 1)

    def test_peek_empty(self):
        self.assertIsNone(self.queue.peek())

    def test_is_full_and_is_empty(self):
        self.assertTrue(self.queue.is_empty())
        self.queue.enqueue(self.vehicle1)
        self.assertFalse(self.queue.is_empty())
        self.queue.enqueue(self.vehicle2)
        self.queue.enqueue(self.vehicle3)
        self.assertTrue(self.queue.is_full())

    def test_get_waiting_vehicles(self):
        self.queue.enqueue(self.vehicle1)
        self.queue.enqueue(self.vehicle2)
        plates = [v.license_plate for v in self.queue.get_waiting_vehicles()]
        self.assertEqual(plates, ["1234", "5678"])

if __name__ == "__main__":
    unittest.main()