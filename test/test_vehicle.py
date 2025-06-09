# test_vehicle.py
import time
from core.vehicle import Vehicle

def test_vehicle_timing():
    """
    Test the Vehicle class by simulating realistic timing events and verifying
    time calculations (queue time, stack time, total time).
    """

    print("Starting Vehicle class test...\n")

    # Create a vehicle instance with a license plate and an owner name
    v = Vehicle("KA01AB1234", "Vikranth")
    print(f"Created: {v}")  # Uses __str__ method for friendly output

    # Simulate the vehicle arrival time as current time
    arrival = time.time()
    v.set_arrival_time(arrival)
    print(f"Arrival Time Set: {v.get_arrival_time()}")

    # Simulate vehicle entering the waiting queue 10 seconds after arrival
    # This models some delay before it is actually placed in the queue
    v.set_queue_entry_time(arrival + 10)
    print(f"Queue Entry Time: {v.get_queue_entry_time()}")

    # Simulate vehicle leaving the waiting queue 70 seconds after queue entry
    # Total time spent in queue is 70 seconds here
    v.set_queue_exit_time(v.get_queue_entry_time() + 70)
    print(f"Queue Exit Time: {v.get_queue_exit_time()}")

    # Simulate vehicle entering the parking stack immediately after queue exit
    # No delay assumed here between queue exit and parking
    v.set_stack_entry_time(v.get_queue_exit_time())
    print(f"Stack Entry Time: {v.get_stack_entry_time()}")

    # Simulate vehicle exiting the parking stack after 120 seconds
    # This models parking duration in the stack (LIFO) structure
    v.set_stack_exit_time(v.get_stack_entry_time() + 120)
    print(f"Stack Exit Time: {v.get_stack_exit_time()}")

    # Simulate final exit from the system 5 seconds after leaving the stack
    # This models any final delay before the vehicle completely leaves
    v.set_exit_time(v.get_stack_exit_time() + 5)
    print(f"Exit Time: {v.get_exit_time()}")

    # Calculate and print time spent in queue by subtracting queue entry and exit
    print("\nTime spent in queue (seconds):", v.time_in_queue())

    # Calculate and print time spent in parking stack by subtracting stack entry and exit
    print("Time spent in stack (seconds):", v.time_in_stack())

    # Calculate and print total time spent in the system (arrival to exit)
    # If arrival/exit times are missing, this falls back to queue + stack time sum
    print("Total time in system (seconds):", v.total_time_in_system())

    # Print full vehicle representation with all time details for verification
    print("\nFull Vehicle Info:")
    print(repr(v))


if __name__ == "__main__":
    # Run the test function when script is executed directly
    test_vehicle_timing()
