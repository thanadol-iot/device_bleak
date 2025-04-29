def parse_weight(data):
    data_hex = data.hex()
    # ตัดเป็น list ทีละ 2 ตัว (byte)
    bytes_list = [data_hex[i:i+2] for i in range(0, len(data_hex), 2)]
    # print(f"Data list: {bytes_list}")
    # ต้องมีอย่างน้อย 5 bytes
    if len(bytes_list) < 9:
        print("Data too short")
        return None, None
    # นับจากท้าย:
    
    weight_hex = bytes_list[4]+bytes_list[3]  
    weight = (int(weight_hex, 16))/100
    
    units = "unknown."
    if bytes_list[8] == '00':
        units = "kg."
    elif bytes_list[8] == '01':
        weight = weight * 2.20462
        units = "lb."
        
    return weight,units
