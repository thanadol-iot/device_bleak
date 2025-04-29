from .parse import parse_spo2_pr

def handle_OxSat(sender, data):
    oxsat_bin, bpm = parse_spo2_pr(data)
    if oxsat_bin and bpm is not None:
        oxsat_decimal = int(oxsat_bin, 2)  # แปลง binary -> decimal
        print(f"SpO2: {oxsat_decimal} %, PR: {bpm} bpm")
    else:
        print("Failed to parse data")