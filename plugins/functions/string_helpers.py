def pad_hexadecimal_to_64bit(hex_string):
    if hex_string:
        return '0x' + hex_string[2:].zfill(16)
    return None

def check_address_in_range(current_address, address_range, base_address):
    #print(" curr_add: " + str(current_address))
    #print(" addr_range: " + str(address_range))
    #print(" base_addr: " + str(base_address))
    if not base_address:
        return 1
    decimal_base_address = int(base_address, 16)
    decimal_current_address = int(current_address, 16)
    decimal_max_address = decimal_base_address + int(address_range)
    #print(" dec_curr_add: " + str(decimal_current_address))
    #print(" dec_base_addr: " + str(decimal_base_address))
    #print(" dec_max_addr: " + str(decimal_max_address))
    if decimal_current_address >= decimal_max_address or decimal_current_address < decimal_base_address:
        print("is not in range")
        return 1
    #print("is in range")
    return 0

