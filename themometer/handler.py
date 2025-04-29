from .parse import parse_temperature

def handle_temperature(sender,data):
    data_hex = data.hex()
    # print(f"Data hex: {data_hex}")
    temp = parse_temperature(data_hex)
    print(f"Temperature is: {temp} °C")