from .parse import parse_temperature

def handle_temperature(sender,data):
    data_hex = data.hex()
    temp = parse_temperature(data_hex)
    
    if temp is None:
        return
    
    print(f"Temperature is: {temp} °C")
    return