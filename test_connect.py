import asyncio
from bleak import BleakClient

# 🔧 แก้ไข MAC Address ของอุปกรณ์ที่ต้องการเชื่อมต่อ
ADDRESS = "D0:25:3C:18:00:6B"  # เปลี่ยนเป็นของคุณ

async def explore_device(address):
    try:
        async with BleakClient(address) as client:
            if not client.is_connected:
                print(f"Failed to connect to {address}")
                return

            print(f"Connected to {address}")

            services = await client.get_services()

            for service in services:
                print(f"\n🔧 Service: {service.uuid} ({service.description})")
                for char in service.characteristics:
                    props = ", ".join(char.properties)
                    print(f"Characteristic: {char.uuid}")
                    print(f"Properties: {props}")

                    if "read" in char.properties:
                        try:
                            value = await client.read_gatt_char(char.uuid)
                            print(f"Value: {value}")
                        except Exception as e:
                            print(f"Read error: {e}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(explore_device(ADDRESS))
