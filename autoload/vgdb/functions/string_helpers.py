def pad_hexadecimal_to_64bit(hex_string):
    if hex_string:
        return '0x' + hex_string[2:].zfill(16)
    return None
