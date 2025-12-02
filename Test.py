def calculate_gas():
    num_stations = int(input("How many gas stations? "))

    all_stations_total = 0

    for s in range(1, num_stations + 1):
        print(f"\n--- Station {s} ---")
        num_pumps = int(input("Number of pumps: "))

        station_total = 0

        for p in range(1, num_pumps + 1):
            print(f"\nPump {p}:")
            initial = float(input("  Initial reading: "))
            final = float(input("  Final reading: "))

            pumped = final - initial
            station_total += pumped

            print(f"  → Pump {p} pumped: {pumped} liters")

        print(f"\nTotal for Station {s}: {station_total} liters")
        all_stations_total += station_total

    print("\n===============================")
    print(f"Grand Total (all stations): {all_stations_total} liters")
    print("===============================")


calculate_gas()
