import asyncio
import os
from bleak import BleakClient, BleakScanner
from dotenv import load_dotenv

from themometer.handler import handle_temperature
from oximetor.handler import handle_OxSat
from weightMachine.handler import handle_weight
from bloodPressureMonitor.handler import handle_bp

load_dotenv()

TARGET_NAME_THEMO = os.getenv("TARGET_NAME_THEMO")
TEMPERATURE_CHAR_UUID = os.getenv("TEMPERATURE_CHAR_UUID")

TARGET_NAME_OXSAT = os.getenv("TARGET_NAME_OXSAT")
OXSAT_CHAR_UUID = os.getenv("OXSAT_CHAR_UUID")

TARGET_NAME_WEIGHT = os.getenv("TARGET_NAME_WEIGHT")
WEIGHT_CHAR_UUID = os.getenv("WEIGHT_CHAR_UUID")

TARGET_NAME_BP = os.getenv("TARGET_NAME_BP")
BP_CHAR_UUID = os.getenv("BP_CHAR_UUID")

connected_devices = set()  # Store connected device addresses globally

async def connect_and_listen(address, device_type):
    global connected_devices

    while True:
        try:
            async with BleakClient(address) as client:
                if not client.is_connected:
                    print(f"Failed to connect to {device_type} ({address}). Retrying...")
                    await asyncio.sleep(5)
                    continue

                print(f"Connected to {device_type} ({address})")

                if device_type == "thermometer":
                    await client.start_notify(TEMPERATURE_CHAR_UUID, handle_temperature)
                elif device_type == "weighing":
                    await client.start_notify(WEIGHT_CHAR_UUID, handle_weight)
                elif device_type == "oximeter":
                    await client.start_notify(OXSAT_CHAR_UUID, handle_OxSat)
                elif device_type == "bloodPressureMonitor":
                    await client.start_notify(BP_CHAR_UUID, handle_bp)

                while client.is_connected:
                    await asyncio.sleep(1)

                print(f"Disconnected from {device_type} ({address}). Will retry.")
                connected_devices.discard(address)
                break  # Exit loop and allow re-discovery

        except Exception as e:
            print(f"[{device_type} - {address}] Error: {e}")
            connected_devices.discard(address)
            await asyncio.sleep(5)
            break  # Allow the scanner to try again

async def find_and_connect():
    global connected_devices

    while True:
        print("Scanning for devices...\n")
        devices = await BleakScanner.discover()
        tasks = []

        for d in devices:
            if d.name:
                if TARGET_NAME_THEMO and (d.address.upper() == TARGET_NAME_THEMO.upper() or d.name == TARGET_NAME_THEMO):
                    if d.address not in connected_devices:
                        print(f"Found Thermometer: {d.name} ({d.address})")
                        tasks.append(connect_and_listen(d.address, "thermometer"))
                        connected_devices.add(d.address)

                elif TARGET_NAME_WEIGHT and (d.address.upper() == TARGET_NAME_WEIGHT.upper() or d.name.lower() == TARGET_NAME_WEIGHT.lower()):
                    if d.address not in connected_devices:
                        print(f"Found Weighing Machine: {d.name} ({d.address})")
                        tasks.append(connect_and_listen(d.address, "weighing"))
                        connected_devices.add(d.address)

                elif TARGET_NAME_OXSAT and (d.address.upper() == TARGET_NAME_OXSAT.upper() or d.name == TARGET_NAME_OXSAT):
                    if d.address not in connected_devices:
                        print(f"Found Oximeter: {d.name} ({d.address})")
                        tasks.append(connect_and_listen(d.address, "oximeter"))
                        connected_devices.add(d.address)

                elif TARGET_NAME_BP and (d.address.upper() == TARGET_NAME_BP.upper() or d.name == TARGET_NAME_BP):
                    if d.address not in connected_devices:
                        print(f"Found Blood Pressure Monitor: {d.name} ({d.address})")
                        tasks.append(connect_and_listen(d.address, "bloodPressureMonitor"))
                        connected_devices.add(d.address)

        if tasks:
            await asyncio.gather(*tasks)

        print("\nNo new targets found or all are connected. Rescanning in 2 seconds...\n")
        await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(find_and_connect())
