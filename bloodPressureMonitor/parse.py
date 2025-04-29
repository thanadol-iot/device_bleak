def parse_bp(data):
    data_hex = data.hex()
    # ตัดเป็น list ทีละ 2 ตัว (byte)
    bytes_list = [data_hex[i:i+2] for i in range(0, len(data_hex), 2)]
    # print(f"Data list: {bytes_list}")
    # ต้องมีอย่างน้อย 5 bytes
    if len(bytes_list) < 15:
        print("Data too short")
        return None, None, None
    # นับจากท้าย:
    
    sys_hex = bytes_list[1]
    sys = int(sys_hex, 16)
    
    dia_hex = bytes_list[3]
    dia = int(dia_hex, 16)
    
    pmin_hex = bytes_list[14]
    pmin = int(pmin_hex, 16)
        
    return sys, dia, pmin
    
