from .parse import parse_weight

def handle_weight(sender,data):
    # สมมุติว่า decode น้ำหนักจาก data
    weight, units = parse_weight(data)

    if weight is None or units is None:
        # print("Received invalid weight data:", data)
        return

    print(f"Weight is: {weight:.2f} {units}")
    return