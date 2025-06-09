# core/vehicle.py
import time

from utils.logger import log_event
class Vehicle:
    """
    Represents a vehicle in the parking system.

    Attributes:
        license_plate (str): Unique identifier for the vehicle.
        owner_name (str, optional): Name of the vehicle owner.
        arrival_time (float): Timestamp when vehicle first arrived (either queue or parking).
        exit_time (float, optional): Timestamp when vehicle finally exits the system.
        queue_entry_time (float, optional): Timestamp when vehicle enters waiting queue.
        queue_exit_time (float, optional): Timestamp when vehicle leaves waiting queue.
        stack_entry_time (float, optional): Timestamp when vehicle enters parking stack.
        stack_exit_time (float, optional): Timestamp when vehicle leaves parking stack.
    """

    def __init__(self, license_plate: str, owner_name: str = None):
        self.license_plate = license_plate
        self.owner_name = owner_name

        # Initialize all time fields to None
        self.arrival_time = None
        self.exit_time = None
        self.queue_entry_time = None
        self.queue_exit_time = None
        self.stack_entry_time = None
        self.stack_exit_time = None

    # Getters and Setters

    def get_license_plate(self) -> str:
        return self.license_plate

    def set_owner_name(self, owner_name: str):
        self.owner_name = owner_name

    def get_owner_name(self) -> str:
        return self.owner_name

    def set_arrival_time(self, timestamp: float = None):
        self.arrival_time = timestamp if timestamp is not None else time.time()

    def get_arrival_time(self) -> float:
        return self.arrival_time

    def set_exit_time(self, timestamp: float = None):
        self.exit_time = timestamp if timestamp is not None else time.time()

    def get_exit_time(self) -> float:
        return self.exit_time

    def set_queue_entry_time(self, timestamp: float = None):
        self.queue_entry_time = timestamp if timestamp is not None else time.time()

    def get_queue_entry_time(self) -> float:
        return self.queue_entry_time

    def set_queue_exit_time(self, timestamp: float = None):
        self.queue_exit_time = timestamp if timestamp is not None else time.time()

    def get_queue_exit_time(self) -> float:
        return self.queue_exit_time

    def set_stack_entry_time(self, timestamp: float = None):
        self.stack_entry_time = timestamp if timestamp is not None else time.time()

    def get_stack_entry_time(self) -> float:
        return self.stack_entry_time

    def set_stack_exit_time(self, timestamp: float = None):
        self.stack_exit_time = timestamp if timestamp is not None else time.time()

    def get_stack_exit_time(self) -> float:
        return self.stack_exit_time

    # Time spent calculations

    def time_in_queue(self) -> float:
        """
        Returns time spent in waiting queue in seconds.
        Returns 0 if timestamps are not set or invalid.
        """
        if self.queue_entry_time is not None and self.queue_exit_time is not None:
            return max(0, self.queue_exit_time - self.queue_entry_time)
        return 0

    def time_in_stack(self) -> float:
        """
        Returns time spent in parking stack in seconds.
        Returns 0 if timestamps are not set or invalid.
        """
        if self.stack_entry_time is not None and self.stack_exit_time is not None:
            return max(0, self.stack_exit_time - self.stack_entry_time)
        return 0

    def total_time_in_system(self) -> float:
        """
        Returns total time vehicle spent in the system (queue + stack).
        Uses exit_time and arrival_time if available, otherwise sums times in queue and stack.
        Returns 0 if insufficient timestamps.
        """
        if self.arrival_time is not None and self.exit_time is not None:
            return max(0, self.exit_time - self.arrival_time)
        else:
            # fallback to sum of queue + stack time
            return self.time_in_queue() + self.time_in_stack()

    def __str__(self):
        owner_info = f", Owner: {self.owner_name}" if self.owner_name else ""
        return f"Vehicle[Plate: {self.license_plate}{owner_info}]"

    def __repr__(self):
        return (f"Vehicle(license_plate='{self.license_plate}', owner_name='{self.owner_name}', \n "
                f"arrival_time={self.arrival_time}, exit_time={self.exit_time}, \n "
                f"queue_entry_time={self.queue_entry_time}, queue_exit_time={self.queue_exit_time}, \n "
                f"stack_entry_time={self.stack_entry_time}, stack_exit_time={self.stack_exit_time})")
