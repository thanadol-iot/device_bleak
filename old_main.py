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

connected_devices = set()

async def connect_and_listen(address, device_type):
    try:
        async with BleakClient(address) as client:
            if not client.is_connected:
                print(f"Failed to connect to {device_type} ({address}).")
                return

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

            print(f"Disconnected from {device_type} ({address}).")
            connected_devices.discard(address)

    except Exception as e:
        print(f"Error with {device_type} ({address}): {e}")
        connected_devices.discard(address)
        await asyncio.sleep(5)

async def detection_callback(device, advertisement_data):
    if device.name is None or device.address in connected_devices:
        return

    if TARGET_NAME_THEMO and (device.name == TARGET_NAME_THEMO or device.address.upper() == TARGET_NAME_THEMO.upper()):
        print(f"Found thermometer: {device.name}")
        connected_devices.add(device.address)
        asyncio.create_task(connect_and_listen(device.address, "thermometer"))

    elif TARGET_NAME_WEIGHT and (device.name.lower() == TARGET_NAME_WEIGHT.lower() or device.address.upper() == TARGET_NAME_WEIGHT.upper()):
        print(f"Found weighing machine: {device.name}")
        connected_devices.add(device.address)
        asyncio.create_task(connect_and_listen(device.address, "weighing"))

    elif TARGET_NAME_OXSAT and (device.name == TARGET_NAME_OXSAT or device.address.upper() == TARGET_NAME_OXSAT.upper()):
        print(f"Found oximeter: {device.name}")
        connected_devices.add(device.address)
        asyncio.create_task(connect_and_listen(device.address, "oximeter"))

    elif TARGET_NAME_BP and (device.name == TARGET_NAME_BP or device.address.upper() == TARGET_NAME_BP.upper()):
        print(f"Found blood pressure monitor: {device.name}")
        connected_devices.add(device.address)
        asyncio.create_task(connect_and_listen(device.address, "bloodPressureMonitor"))

async def scan_for_devices():
    scanner = BleakScanner(detection_callback)
    async with scanner:
        print("Scanning for BLE devices... Press Ctrl+C to stop.")
        await asyncio.Future()  # Run forever

async def main():
    await scan_for_devices()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Scan stopped by user.")
