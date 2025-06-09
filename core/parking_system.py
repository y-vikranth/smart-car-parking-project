# core/parking_system.py

from utils.logger import log_event
from core.parking_lot import ParkingLot
from core.waiting_queue import WaitingQueue
from core.vehicle import Vehicle


class ParkingSystem:
    """
    Manages vehicle flow between the ParkingLot (stack) and WaitingQueue (queue).
    Handles vehicle arrivals, departures, and reporting.
    """

    def __init__(self, parking_capacity: int, queue_capacity: int):
        self.parking_lot = ParkingLot(parking_capacity)
        self.waiting_queue = WaitingQueue(queue_capacity)
        #self.active_vehicles = {}  # Dictionary to store all active vehicles by license_plate

    def vehicle_arrives(self, vehicle: Vehicle) -> bool:
        """
            Handles the arrival of a vehicle object.
            Returns True if vehicle added successfully, False if already in the system or no space.
        """
        if self.is_vehicle_in_system(vehicle.license_plate):
            print(f"Vehicle {vehicle.license_plate} is already in the system.")
            return False

        vehicle.set_arrival_time()

        if not self.parking_lot.is_full():
            self.parking_lot.park_vehicle(vehicle)
            print(f"Vehicle {vehicle.license_plate} parked directly.")
            return True

        elif not self.waiting_queue.is_full():
            self.waiting_queue.enqueue(vehicle)
            print(f"Parking full. Vehicle {vehicle.license_plate} added to waiting queue.")
            return True

        else:
            print(f"Parking and waiting queue full. Vehicle {vehicle.license_plate} denied entry.")
            return False

    def vehicle_departs(self, license_plate: str) -> bool:
        """
        Handles the departure of a vehicle from the system using the Vehicle object.
        Steps:
            1. Checks if the vehicle is in the parking lot.
            2. If found, removes it from the stack, sets exit time.
            3. If not in parking, checks the waiting queue.
            4. If found in queue, removes it, sets exit time.
            5. If not found in either, returns False.
            6. If a vehicle is removed from the parking lot, try to move a waiting vehicle into parking.


        Args:
            license_plate: The license plate of the vehicle to be removed from parking or waiting queue.

        Returns:
            bool: True if vehicle was found and removed, False otherwise.
        """

        # ✅ Step 1: Check if the vehicle is in the parking lot (stack)
        if any(vehicle.get_license_plate() == license_plate for vehicle in self.parking_lot.get_parked_vehicles()):
            removed_vehicle = self.parking_lot.leave_vehicle(license_plate)

            if removed_vehicle:
                removed_vehicle.set_exit_time()  # System exit time

                # 🔄 Step 2: After one vehicle leaves the stack, check if someone is waiting in queue
                if not self.waiting_queue.is_empty() and not self.parking_lot.is_full():
                    next_vehicle = self.waiting_queue.dequeue()
                    self.parking_lot.park_vehicle(next_vehicle)  # Move from queue to stack

                return True  # ✅ Vehicle removed from parking lot

        # 🕵️ Step 3: If not in parking lot, check if it's in the waiting queue
        waiting_vehicles = self.waiting_queue.get_waiting_vehicles()

        for i, vehicle in enumerate(waiting_vehicles):
            if vehicle.get_license_plate() == license_plate:
                vehicle.set_queue_exit_time()
                vehicle.set_exit_time()

                # ❌ Remove directly from deque at index i
                del self.waiting_queue.queue[i]
                return True  # ✅ Vehicle removed from waiting queue

        # ❌ Step 4: Vehicle not found anywhere
        return False

    def lookup_vehicle(self, license_plate: str) -> str:
        """
        Checks if a vehicle is in parking lot or waiting queue.
        Returns its current status.
        :type license_plate: str
        """

        if not self.is_vehicle_in_system(license_plate):
            return f"Vehicle {license_plate} not found."
        else:
            for vehicle in self.parking_lot.get_parked_vehicles():
                if vehicle.get_license_plate() == license_plate:
                    log_event(f"Lookup for Vehicle {license_plate}: Currently Parked.")
                    return f"Vehicle {license_plate} is currently parked."

            for vehicle in self.waiting_queue.get_waiting_vehicles():
                if vehicle.get_license_plate() == license_plate:
                    log_event(f"Lookup for Vehicle {license_plate}: Currently in Waiting Queue.")
                    return f"Vehicle {license_plate} is currently in Waiting Queue."
            return f"Vehicle {license_plate} not found."

    def get_system_status(self) -> str:
        """
        Returns an overview of parking lot and waiting queue.
        """
        return (
            f"Parking Lot: {self.parking_lot.get_stack_size()}/{self.parking_lot.get_capacity()} occupied\n"
            f"Waiting Queue: {self.waiting_queue.size()}/{self.waiting_queue.max_size} waiting"
        )

    def is_vehicle_in_system(self, license_plate: str) -> bool:
        # Check parking lot
        for v in self.parking_lot.get_parked_vehicles():
            if v.license_plate == license_plate:
                return True

        # Check waiting queue
        for v in self.waiting_queue.get_waiting_vehicles():
            if v.license_plate == license_plate:
                return True

        return False

    def get_parking_lot_status(self) -> str:
        """
        Returns a multi-line string showing:
        - Number of vehicles currently parked.
        - Total capacity of the parking lot.
        - List of parked vehicles with formatted license plate and owner name.
        """
        parked_vehicles = self.parking_lot.get_parked_vehicles()
        total_capacity = self.parking_lot.get_capacity()
        current_count = len(parked_vehicles)

        # Header lines
        lines = []
        lines.append(f"Vehicles Parked: {current_count}")
        lines.append(f"Total Capacity: {total_capacity}\n")

        # Details of parked vehicles
        if not parked_vehicles:
            lines.append("No vehicles are currently parked.")
        else:
            lines.append("Parked Vehicle List:")
            for i, vehicle in enumerate(parked_vehicles, start=1):
                lines.append(f"{i}. License Plate: {vehicle.get_license_plate()} | Owner: {vehicle.get_owner_name()}")

        return "\n".join(lines)

    def get_waiting_queue_status(self) -> str:
        """
        Returns a multi-line string showing:
        - Number of vehicles currently waiting.
        - Total capacity of the waiting queue.
        - List of waiting vehicles with formatted license plate and owner name.
        """
        waiting_vehicles = self.waiting_queue.get_waiting_vehicles()
        total_capacity = self.waiting_queue.max_size
        current_count = len(waiting_vehicles)

        # Header lines
        lines = []
        lines.append(f"Vehicles Waiting: {current_count}")
        lines.append(f"Total Capacity: {total_capacity}\n")

        # Details of parked vehicles
        if not waiting_vehicles:
            lines.append("No vehicles are currently waiting.")
        else:
            lines.append("Waiting Vehicle List:")
            for i, vehicle in enumerate(waiting_vehicles, start=1):
                lines.append(f"{i}. License Plate: {vehicle.get_license_plate()} | Owner: {vehicle.get_owner_name()}")

        return "\n".join(lines)

