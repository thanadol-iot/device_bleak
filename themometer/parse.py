def parse_temperature(data):
    bytes_list = [data[i:i+2] for i in range(0, len(data), 2)]
    hex_string = bytes_list[2] + bytes_list[1]
    decimal_value = int(hex_string, 16)
    return decimal_value / 100