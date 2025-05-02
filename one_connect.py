import asyncio
import json
from bleak import BleakClient, BleakScanner

TARGET_NAME = "Yuwell BO-YX310-21CA"
TEMPERATURE_CHAR_UUID = "00002a1c-0000-1000-8000-00805f9b34fb"
OXSAT_CHAR_UUID = "0000ffe4-0000-1000-8000-00805f9b34fb"

def parse_temperature(data):
    bytes_list = [data[i:i+2] for i in range(0, len(data), 2)]
    hex_string = bytes_list[2] + bytes_list[1]
    decimal_value = int(hex_string, 16)
    return decimal_value / 100

def handle_temperature(data):
    data_hex = data.hex()
    temp = parse_temperature(data_hex)
    print(f"Temperature is: {temp} °C")
    
def parse_spo2_pr(data):
    data_hex = data.hex()
    # print(f"data_hex: {data_hex}")
    # ตัดเป็น list ทีละ 2 ตัว (byte)
    bytes_list = [data_hex[i:i+2] for i in range(0, len(data_hex), 2)]
    
    # print(f"Data list: {bytes_list}")

    # ต้องมีอย่างน้อย 5 bytes
    if len(bytes_list) < 5:
        print("Data too short")
        return None, None

    # นับจากท้าย:
    oxsat_hex = bytes_list[-5]  # ตำแหน่งที่ 5 (OxSat)
    bpm_hex = bytes_list[-6]    # ตำแหน่งที่ 4 (bpm)
    # print(f"OxSat: {oxsat_hex}, PR: {bpm_hex}")

    # แปลงค่าจาก hex เป็น integer
    oxsat_decimal = int(oxsat_hex, 16)
    bpm_decimal = int(bpm_hex, 16)

    # OxSat ต้องแปลงเป็น binary string
    oxsat_binary = format(oxsat_decimal, '08b')  # 8 bits

    return oxsat_binary, bpm_decimal

def handle_OxSat(sender, data):
    oxsat_bin, bpm = parse_spo2_pr(data)
    if oxsat_bin and bpm is not None:
        oxsat_decimal = int(oxsat_bin, 2)  # แปลง binary -> decimal
        print(f"SpO2: {oxsat_decimal} %, PR: {bpm} bpm")
    else:
        print("Failed to parse data")

async def connect_and_listen(address):
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

                # print(f"Connected to {address}!")
                await client.start_notify(OXSAT_CHAR_UUID, handle_OxSat)

                while client.is_connected:
                    await asyncio.sleep(1)

                print("Disconnected. Reconnecting...")

        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(5)

async def find_and_connect():
    while True:
        print("Scanning for devices...\n")
        devices = await BleakScanner.discover()
        for d in devices:
            if d.name:  # Only include if name is not None or empty
                print(f"    address : {d.address}, device name : {d.name}")
            
            if d.address.upper() == TARGET_NAME.upper() or d.name == TARGET_NAME:
                print(f"Found target device: {d.name}")
                await connect_and_listen(d.address)
                return

        print("\nTarget not found. Scanning again in 5 seconds...")
        await asyncio.sleep(5)

asyncio.run(find_and_connect())