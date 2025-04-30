from .parse import parse_bp

def handle_bp(sender,data):
    sys, dia, pmin = parse_bp(data)
    if sys is None or dia is None or pmin is None:
        return
        
    print(f"SYS : {sys}, DIA : {dia}, PULSE : {pmin}")
    return