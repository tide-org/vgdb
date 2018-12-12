def pad_hexadecimal_to_64bit(self, hex_string):
    return '0x' + hex_string[2:].zfill(16)
