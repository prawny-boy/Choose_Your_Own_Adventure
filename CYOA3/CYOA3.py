def encode_base64(data):
    base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    binary_string = ''.join([format(ord(char), '08b') for char in data])
    padding = len(binary_string) % 6
    if padding != 0:
        binary_string += '0' * (6 - padding)
    encoded_string = ''.join([base64_chars[int(binary_string[i:i+6], 2)] for i in range(0, len(binary_string), 6)])
    padding_length = (4 - len(encoded_string) % 4) % 4
    encoded_string += '=' * padding_length
    return encoded_string

# Base64 decoding function
def decode_base64(encoded_data):
    base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    encoded_data = encoded_data.rstrip('=')
    binary_string = ''.join([format(base64_chars.index(char), '06b') for char in encoded_data])
    decoded_string = ''.join([chr(int(binary_string[i:i+8], 2)) for i in range(0, len(binary_string), 8)])
    return decoded_string


def encode_base128(data):
    base128_chars = ''.join([chr(i) for i in range(128)])
    binary_string = ''.join([format(ord(char), '08b') for char in data])
    padding = len(binary_string) % 7
    if padding != 0:
        binary_string += '0' * (7 - padding)
    encoded_string = ''.join([base128_chars[int(binary_string[i:i+7], 2)] for i in range(0, len(binary_string), 7)])
    return encoded_string

# Base128 decoding function
def decode_base128(encoded_data):
    base128_chars = ''.join([chr(i) for i in range(128)])
    binary_string = ''.join([format(base128_chars.index(char), '07b') for char in encoded_data])
    decoded_string = ''.join([chr(int(binary_string[i:i+8], 2)) for i in range(0, len(binary_string), 8)])
    return decoded_string

def encode_base24(data):
    base24_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    binary_string = ''.join([format(ord(char), '08b') for char in data])
    padding = len(binary_string) % 5
    if padding != 0:
        binary_string += '0' * (5 - padding)
    encoded_string = ''.join([base24_chars[int(binary_string[i:i+5], 2)] for i in range(0, len(binary_string), 5)])
    padding_length = (8 - len(encoded_string) % 8) % 8
    encoded_string += '=' * padding_length
    return encoded_string

# Base24 decoding function
def decode_base24(encoded_data):
    base24_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    encoded_data = encoded_data.rstrip('=')
    binary_string = ''.join([format(base24_chars.index(char), '05b') for char in encoded_data])
    decoded_string = ''.join([chr(int(binary_string[i:i+8], 2)) for i in range(0, len(binary_string), 8)])
    return decoded_string

def decode(data:str) -> str:
    data = decode_base128(data)
    data = decode_base24(data)
    data = decode_base64(data)
    return data

def encode(data:str) -> str:
    data = encode_base64(data)
    data = encode_base24(data)
    data = encode_base128(data)
    return data
