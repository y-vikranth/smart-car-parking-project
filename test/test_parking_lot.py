# tests/test_parking_lot.py

import unittest
from core.parking_lot import ParkingLot
from core.vehicle import Vehicle

class TestParkingLot(unittest.TestCase):

    def setUp(self):
        """
        This method runs before each test.
        It initializes a ParkingLot instance with capacity 3,
        so each test starts with a fresh parking lot.
        """
        self.parking_lot = ParkingLot(capacity=3)

    def test_park_vehicle_success(self):
        """
        Test parking a single vehicle in an empty parking lot.
        It should succeed and the vehicle should be added to the stack.
        """
        v1 = Vehicle("ABC1234")  # Create a vehicle object
        result = self.parking_lot.park_vehicle(v1)  # Try to park it
        self.assertTrue(result)  # Expect True because space is available
        self.assertEqual(len(self.parking_lot.stack), 1)  # Stack size should be 1
        self.assertEqual(self.parking_lot.stack[-1], v1)  # The vehicle should be on top

    def test_park_vehicle_full(self):
        """
        Test parking vehicles until capacity is reached,
        then attempt to park one more vehicle, which should fail.
        """
        # Park vehicles up to capacity
        for i in range(3):
            self.parking_lot.park_vehicle(Vehicle(f"CAR{i}"))
        v_extra = Vehicle("EXTRA1")  # Vehicle beyond capacity
        result = self.parking_lot.park_vehicle(v_extra)
        self.assertFalse(result)  # Should return False (no space)
        self.assertEqual(len(self.parking_lot.stack), 3)  # Stack remains full
        self.assertNotIn(v_extra, self.parking_lot.stack)  # Extra vehicle not in stack

    def test_leave_vehicle_top(self):
        """
        Test removing the vehicle at the top of the stack.
        This is the simplest removal case.
        """
        v1 = Vehicle("TOP123")
        self.parking_lot.park_vehicle(v1)
        removed = self.parking_lot.leave_vehicle("TOP123")  # Remove vehicle by license plate
        self.assertEqual(removed, v1)  # Removed vehicle should be the one we parked
        self.assertTrue(self.parking_lot.is_empty())  # Parking lot should be empty after removal

    def test_leave_vehicle_middle(self):
        """
        Test removing a vehicle from the middle of the stack.
        Vehicles above it must be temporarily removed and restored.
        Checks that order is maintained and the correct vehicle is removed.
        """
        # Park three vehicles
        v1 = Vehicle("CAR1")
        v2 = Vehicle("CAR2")
        v3 = Vehicle("CAR3")
        self.parking_lot.park_vehicle(v1)
        self.parking_lot.park_vehicle(v2)
        self.parking_lot.park_vehicle(v3)

        # Remove the middle vehicle (CAR2)
        removed = self.parking_lot.leave_vehicle("CAR2")
        self.assertEqual(removed.license_plate, "CAR2")  # Confirm correct vehicle removed

        # Confirm CAR2 is no longer in the stack
        plates = [v.license_plate for v in self.parking_lot.stack]
        self.assertNotIn("CAR2", plates)

        # Stack size reduced by one
        self.assertEqual(len(self.parking_lot.stack), 2)

        # Ensure the order of remaining vehicles is correct:
        # CAR3 should still be on top and CAR1 at the bottom
        self.assertEqual(self.parking_lot.stack[-1].license_plate, "CAR3")
        self.assertEqual(self.parking_lot.stack[0].license_plate, "CAR1")

    def test_leave_vehicle_not_found(self):
        """
        Test removing a vehicle that does not exist in the stack.
        Should return None and parking lot state remains unchanged.
        """
        v1 = Vehicle("CAR1")
        self.parking_lot.park_vehicle(v1)
        removed = self.parking_lot.leave_vehicle("NOTFOUND")  # Vehicle not present
        self.assertIsNone(removed)  # Removal should fail gracefully
        self.assertEqual(len(self.parking_lot.stack), 1)  # Stack remains unchanged

    def test_get_parked_vehicles(self):
        """
        Test retrieval of the list of parked vehicles in the order
        from bottom to top of the stack.
        """
        v1 = Vehicle("CAR1")
        v2 = Vehicle("CAR2")
        self.parking_lot.park_vehicle(v1)
        self.parking_lot.park_vehicle(v2)
        vehicles = self.parking_lot.get_parked_vehicles()
        self.assertEqual(vehicles, [v1, v2])  # Order should be preserved

if __name__ == "__main__":
    unittest.main()
