from .parse import parse_weight

def handle_weight(sender,data):
    weight,units = parse_weight(data)
    print(f"Weight is: {weight:.2f} {units}")