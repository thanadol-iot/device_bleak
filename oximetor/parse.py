def parse_spo2_pr(data):
    data_hex = data.hex()
    # print(f"data_hex: {data_hex}")
    # ตัดเป็น list ทีละ 2 ตัว (byte)
    bytes_list = [data_hex[i:i+2] for i in range(0, len(data_hex), 2)]
    
    # print(f"Data list: {bytes_list}")

    # ต้องมีอย่างน้อย 5 bytes
    if len(bytes_list) < 6:
        # print("Data too short")
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