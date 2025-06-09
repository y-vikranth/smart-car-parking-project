# core/waiting_queue.py

from utils.logger import log_event
from collections import deque
import time
from core.vehicle import Vehicle

class WaitingQueue:
    """
    Represents a queue (FIFO) for vehicles waiting for a parking spot.
    """

    def __init__(self, max_size: int):
        self.queue = deque()
        self.max_size = max_size

    def enqueue(self, vehicle: Vehicle) -> bool:
        """
        Adds a vehicle to the queue if space is available.
        Sets queue entry time.
        Returns True if added, False if queue is full.
        """
        if self.is_full():
            return False
        vehicle.set_queue_entry_time()
        self.queue.append(vehicle)
        return True

    def dequeue(self) -> Vehicle:
        """
        Removes and returns the vehicle at the front of the queue.
        Sets queue exit time.
        Returns None if the queue is empty.
        """
        if self.is_empty():
            return None
        vehicle = self.queue.popleft()
        vehicle.set_queue_exit_time()
        return vehicle

    def peek(self) -> Vehicle:
        """
        Returns the vehicle at the front of the queue without removing it.
        Returns None if queue is empty.
        """
        if self.is_empty():
            return None
        return self.queue[0]

    def is_full(self) -> bool:
        """
        Checks if the queue has reached maximum capacity.
        """
        return len(self.queue) >= self.max_size

    def is_empty(self) -> bool:
        """
        Checks if the queue is empty.
        """
        return len(self.queue) == 0

    def size(self) -> int:
        """
        Returns the current number of vehicles in the queue.
        """
        return len(self.queue)

    def get_waiting_vehicles(self) -> list:
        """
        Returns a list of all vehicles currently in the queue.
        """
        return list(self.queue)

    def __str__(self):
        return f"WaitingQueue(size={self.size()}, vehicles={[str(v) for v in self.queue]})"
