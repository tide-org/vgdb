import string

def pad_hexadecimal_to_64bit(hex_string):
    if hex_string:
        return '0x' + hex_string[2:].zfill(16)
    return None

def check_address_in_range(current_address, address_range, base_address):
    if not base_address:
        return 1
    decimal_base_address = int(base_address, 16)
    decimal_current_address = int(current_address, 16)
    decimal_max_address = decimal_base_address + int(address_range)
    if decimal_current_address >= decimal_max_address or decimal_current_address < decimal_base_address:
        return 0
    return 1
