# cli/interface.py

from core.parking_system import ParkingSystem
from core.vehicle import Vehicle


def display_menu():
    print("\n🚗 Smart Parking Lot Simulation 🚗")
    print("1. Park a vehicle")
    print("2. Remove a vehicle")
    print("3. View parking lot status")
    print("4. View waiting queue")
    print("5. Lookup a vehicle")
    print("6. Exit")
    choice = input("Enter your choice (1-6): ")
    return choice

def run_parking_system():
    system = ParkingSystem(2, 2)

    while True:
        choice = display_menu()
        if choice == '1':
            print("\n[Add Vehicle]")
            license_plate = input("Enter license plate: ").strip().upper()
            owner_name = input("Enter owner name (optional): ").strip()

            if not license_plate:
                print("License plate cannot be empty.")

            else:
                vehicle = Vehicle(license_plate, owner_name if owner_name else None)
                system.vehicle_arrives(vehicle)

        elif choice == '2':

            print("\n--- Vehicle Departure ---")

            license_plate = input("Enter license plate of the departing vehicle: ").strip().upper()

            if not license_plate:
                print("License plate cannot be empty.")

                continue

            # Attempt to remove vehicle from the system

            success = system.vehicle_departs(license_plate)

            if success:

                print(f"Vehicle with license plate '{license_plate}' has departed the system.")

            else:

                print(f"No active vehicle with license plate '{license_plate}' found in the system.")

        elif choice == '3':
            # print(system.get_system_status())
            print(system.get_parking_lot_status())

        elif choice == '4':
            print(system.get_waiting_queue_status())

        elif choice == '5':
            plate = input("Enter vehicle license plate to lookup: ").strip().upper()
            if not plate:
                print("License plate cannot be empty.")
                continue
            print(system.lookup_vehicle(plate))

        elif choice == '6':
            print("✅ Exiting Smart Parking Lot. Goodbye!")
            break

        else:
            print("❌ Invalid choice. Please enter a number between 1 and 6.")
