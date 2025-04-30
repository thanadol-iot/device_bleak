from .parse import parse_bp

def handle_bp(sender,data):
    sys, dia, pmin = parse_bp(data)
    print(f"SYS : {sys}, DIA : {dia}, PULSE : {pmin}")
    return