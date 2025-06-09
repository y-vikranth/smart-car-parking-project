import unittest
import time
from core.parking_system import ParkingSystem

class TestParkingSystem(unittest.TestCase):

    def setUp(self):
        self.system = ParkingSystem(parking_capacity=2, queue_capacity=2)

    def test_vehicle_arrival_parking_available(self):
        result = self.system.vehicle_arrives("KA01AB1234", "Alice")
        self.assertIn("parked", result)

    def test_vehicle_arrival_parking_full_queue_available(self):
        self.system.vehicle_arrives("KA01AB1234")
        self.system.vehicle_arrives("KA01AB5678")
        result = self.system.vehicle_arrives("KA01AB9999")
        self.assertIn("waiting queue", result)

    def test_vehicle_arrival_both_full(self):
        # Fill parking
        self.system.vehicle_arrives("KA01AB0001")
        self.system.vehicle_arrives("KA01AB0002")

        # Fill waiting queue
        self.system.vehicle_arrives("KA01AB0003")
        self.system.vehicle_arrives("KA01AB0004")
        self.system.vehicle_arrives("KA01AB0005")  # Queue now full

        # Now this vehicle should be rejected
        result = self.system.vehicle_arrives("KA01AB1111")
        self.assertIn("cannot be accommodated", result)

    def test_vehicle_departure_from_parking(self):
        self.system.vehicle_arrives("KA01AB1234")
        result = self.system.vehicle_departs("KA01AB1234")
        self.assertIn("exited the parking lot", result)

    def test_vehicle_departure_promotes_from_queue(self):
        self.system.vehicle_arrives("KA01AB1234")
        self.system.vehicle_arrives("KA01AB5678")
        self.system.vehicle_arrives("KA01AB9999")  # goes to queue
        result = self.system.vehicle_departs("KA01AB1234")
        self.assertIn("moved from queue to parking", result)

    def test_vehicle_departure_from_queue(self):
        self.system.vehicle_arrives("KA01AB1234")
        self.system.vehicle_arrives("KA01AB5678")
        self.system.vehicle_arrives("KA01AB9999")  # goes to queue
        result = self.system.vehicle_departs("KA01AB9999")
        self.assertIn("removed from waiting queue", result)

    def test_lookup_vehicle_status(self):
        self.system.vehicle_arrives("KA01AB1234")
        result = self.system.lookup_vehicle("KA01AB1234")
        self.assertIn("currently parked", result)

    def test_lookup_vehicle_not_found(self):
        result = self.system.lookup_vehicle("KA01ZZ0000")
        self.assertIn("not found", result)

    def test_generate_parking_report_empty(self):
        result = self.system.generate_parking_report()
        self.assertIn("No vehicles have exited yet", result)

    def test_generate_parking_report_with_data(self):
        self.system.vehicle_arrives("KA01AB1234")
        time.sleep(1)
        self.system.vehicle_departs("KA01AB1234")
        report = self.system.generate_parking_report()
        self.assertIn("Vehicle KA01AB1234", report)

    def test_get_system_status(self):
        self.system.vehicle_arrives("KA01AB1234")
        status = self.system.get_system_status()
        self.assertIn("Parking Lot", status)
        self.assertIn("Waiting Queue", status)

if __name__ == '__main__':
    unittest.main()