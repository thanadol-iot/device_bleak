import asyncio
import json
import os
from bleak import BleakClient, BleakScanner
from dotenv import load_dotenv

from themometer.handler import handle_temperature
from oximetor.handler import handle_OxSat
from weightMachine.handler import handle_weight
from bloodPressureMonitor.handler import handle_bp

load_dotenv()  # Loads from .env into environment

TARGET_NAME_THEMO = os.getenv("TARGET_NAME_THEMO")
TEMPERATURE_CHAR_UUID = os.getenv("TEMPERATURE_CHAR_UUID")

TARGET_NAME_OXSAT = os.getenv("TARGET_NAME_OXSAT")
WEIGHT_CHAR_UUID = os.getenv("WEIGHT_CHAR_UUID")

TARGET_NAME_WEIGHT = os.getenv("TARGET_NAME_WEIGHT")
OXSAT_CHAR_UUID = os.getenv("OXSAT_CHAR_UUID")

TARGET_NAME_BP = os.getenv("TARGET_NAME_BP")
BP_CHAR_UUID = os.getenv("BP_CHAR_UUID")

async def connect_and_listen(address, device_type):
    try:
        async with BleakClient(address) as client:
            if not client.is_connected:
                print(f"Failed to connect to {device_type} ({address}). Retrying...")
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

    except Exception as e:
        print(f"Error with {device_type} ({address}): {e}")
        await asyncio.sleep(5)

async def scan_for_devices(connected_devices):
    while True:
        print("Scanning for devices...\n")
        devices = await BleakScanner.discover()  # Scan for new devices
        tasks = []

        for d in devices:
            if d.name:
                # เชื่อมต่อกับ Thermometer
                if TARGET_NAME_THEMO:
                    if (d.address.upper() == TARGET_NAME_THEMO.upper() or d.name == TARGET_NAME_THEMO) and d.address not in connected_devices:
                        print(f"Found target Thermometer: {d.name}")
                        tasks.append(asyncio.create_task(connect_and_listen(d.address, "thermometer")))
                        connected_devices.add(d.address)

                # เชื่อมต่อกับ Weighing Machine
                if TARGET_NAME_WEIGHT:
                    if (d.address.upper() == TARGET_NAME_WEIGHT.upper() or d.name.lower() == TARGET_NAME_WEIGHT.lower()) and d.address not in connected_devices:
                        print(f"Found target Weighing Machine: {d.name}")
                        tasks.append(asyncio.create_task(connect_and_listen(d.address, "weighing")))
                        connected_devices.add(d.address)

                # เชื่อมต่อกับ Oximeter
                if TARGET_NAME_OXSAT:
                    if (d.address.upper() == TARGET_NAME_OXSAT.upper() or d.name == TARGET_NAME_OXSAT) and d.address not in connected_devices:
                        print(f"Found target Oximeter: {d.name}")
                        tasks.append(asyncio.create_task(connect_and_listen(d.address, "oximeter")))
                        connected_devices.add(d.address)

                # เชื่อมต่อกับ bloodPressureMonitor
                if TARGET_NAME_BP:
                    if (d.address.upper() == TARGET_NAME_BP.upper() or d.name == TARGET_NAME_BP) and d.address not in connected_devices:
                        print(f"Found target bloodPressureMonitor: {d.name}")
                        tasks.append(asyncio.create_task(connect_and_listen(d.address, "bloodPressureMonitor")))
                        connected_devices.add(d.address)
        await asyncio.sleep(5)  # Wait for 5 seconds before scanning again

async def find_and_connect():
    connected_devices = set()

    # เริ่มการสแกนอุปกรณ์ในลูปที่แยกต่างหาก
    scan_task = asyncio.create_task(scan_for_devices(connected_devices))

    # รอจนกว่า scan_task จะเสร็จ
    await scan_task

asyncio.run(find_and_connect())
