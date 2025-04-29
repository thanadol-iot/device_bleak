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

async def connect_and_listen(address,device_type):
    while True:
        try:
            async with BleakClient(address) as client:
                if not client.is_connected:
                    print("Failed to connect. Retrying...")
                    await asyncio.sleep(5)
                    continue
                
                # Get all services and characteristics
                # services = await client.get_services()
                # print("Available Services and Characteristics:")
                # for service in services:
                #     service_name = service.description if service.description else "Unknown Service"
                #     print(f"Service: {service.uuid} ({service_name})")
                #     for char in service.characteristics:
                #         char_name = char.description if char.description else "Unknown Characteristic"
                #         print(f"  Characteristic: {char.uuid} ({char_name}) [{','.join(char.properties)}]")
                
                # print(f"Connected to {device_type} ({address})!")

                if device_type == "thermometer":
                    await client.start_notify(TEMPERATURE_CHAR_UUID, handle_temperature)
                elif device_type == "weighing":
                    await client.start_notify(WEIGHT_CHAR_UUID, handle_weight)
                elif device_type == "oximeter":
                    await client.start_notify(OXSAT_CHAR_UUID, handle_OxSat)
                elif device_type == "bloodPressureMonitor":
                    await client.start_notify(BP_CHAR_UUID, handle_bp)                # Blood Pressure Monitor

                while client.is_connected:
                    await asyncio.sleep(1)

                print(f"Disconnected from {device_type}. Reconnecting...")

        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(5)

async def find_and_connect():
    connected_devices = set()

    while True:
        print("Scanning for devices...\n")
        devices = await BleakScanner.discover()
        tasks = []

        for d in devices:
            if d.name:
                # print(f"    address : {d.address}, device name : {d.name}")
                # Thermometer
                if TARGET_NAME_THEMO:
                    if (d.address.upper() == TARGET_NAME_THEMO.upper() or d.name == TARGET_NAME_THEMO) and d.address not in connected_devices:
                        # print(f"Found target Thermometer: {d.name}")
                        tasks.append(connect_and_listen(d.address, "thermometer"))
                        connected_devices.add(d.address)

                # Weighing Machine
                if TARGET_NAME_WEIGHT:
                    if (d.address.upper() == TARGET_NAME_WEIGHT.upper() or d.name.lower() == TARGET_NAME_WEIGHT.lower()) and d.address not in connected_devices:
                        # print(f"Found target Weighing Machine: {d.name}")
                        tasks.append(connect_and_listen(d.address, "weighing"))
                        connected_devices.add(d.address)

                # Oximeter
                if TARGET_NAME_OXSAT:
                    if (d.address.upper() == TARGET_NAME_OXSAT.upper() or d.name == TARGET_NAME_OXSAT) and d.address not in connected_devices:
                        # print(f"Found target Oximeter: {d.name}")
                        tasks.append(connect_and_listen(d.address, "oximeter"))
                        connected_devices.add(d.address)
                    
                # bloodPressureMonitor
                if TARGET_NAME_BP:
                    if (d.address.upper() == TARGET_NAME_BP.upper() or d.name == TARGET_NAME_BP) and d.address not in connected_devices:
                        # print(f"Found target bloodPressureMonitor: {d.name}")
                        tasks.append(connect_and_listen(d.address, "bloodPressureMonitor"))
                        connected_devices.add(d.address)

        if tasks:
            await asyncio.gather(*tasks)

        print("\nTarget not found or already connected. Scanning again in 5 seconds...")
        await asyncio.sleep(5)


asyncio.run(find_and_connect())
