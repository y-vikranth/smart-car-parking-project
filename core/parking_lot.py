# core/parking_lot.py

from utils.logger import log_event
from core.vehicle import Vehicle

class ParkingLot:
    """
    Parking lot implemented as a stack with fixed capacity.
    Manages vehicles using LIFO principle.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity            # Maximum parking slots
        self.stack = []                    # Stack to hold vehicles (list used as stack)

    def is_full(self) -> bool:
        """Returns True if parking lot is full."""
        return len(self.stack) >= self.capacity

    def is_empty(self) -> bool:
        """Returns True if parking lot is empty."""
        return len(self.stack) == 0

    # This function returns the capacity of the parking lot
    def get_capacity(self) -> int:
        return self.capacity

    def park_vehicle(self, vehicle: Vehicle) -> bool:
        """
        Attempts to park a vehicle.
        Returns True if successful, False if parking is full.
        """
        if self.is_full():
            return False
        self.stack.append(vehicle)
        # Set vehicle's stack entry time here if desired
        vehicle.set_stack_entry_time()
        return True

    def leave_vehicle(self, license_plate: str) -> Vehicle:
        """
        Removes the vehicle with the given license plate from the parking stack.
        If the vehicle is not on top, temporarily removes vehicles above it and replaces them after removal.
        Returns the removed Vehicle if found and removed, else None.
        """
        temp_stack = []


        removed_vehicle = None

        # Recursive/iterative search to find and remove the vehicle
        while self.stack:
            # Pop the top vehicle from the parking stack
            top_vehicle = self.stack.pop()

            # Check if this is the vehicle we want to remove
            if top_vehicle.license_plate == license_plate:
                # Found the vehicle to remove
                removed_vehicle = top_vehicle

                # Mark the exit time when the vehicle leaves the stack
                removed_vehicle.set_stack_exit_time()

                # Stop searching since vehicle has been removed
                break
            else:
                # This is not the vehicle to remove,
                # temporarily hold it in another stack (temp_stack)
                # so we can restore it later after removal
                temp_stack.append(top_vehicle)

        # Now that the target vehicle has been removed (or not found),
        # put back all other vehicles from temp_stack back onto the original stack
        # This restores the order as it was before the removal operation
        while temp_stack:
            vehicle_to_restore = temp_stack.pop()
            self.stack.append(vehicle_to_restore)

        # Return the removed vehicle if found, or None if not found
        return removed_vehicle

    def get_parked_vehicles(self) -> list:
        """
        Returns a list of all vehicles currently parked, from bottom to top of the stack.
        """
        return list(self.stack)

    # Returns the current number of parked vehicles
    def get_stack_size(self) -> int:
        return len(self.stack)

    def __str__(self):
        return f"ParkingLot(capacity={self.capacity}, parked={len(self.stack)})"

    def __repr__(self):
        return f"ParkingLot(capacity={self.capacity}, stack={self.stack})"
