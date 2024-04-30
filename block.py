import time
import hashlib

def hash256(msg):
    hashp = hashlib.sha256(hashlib.sha256(bytes.fromhex(msg)).digest()).digest()
    return hashp.hex()
def int_to_little_endian_hex(num):
    return num.to_bytes(4, byteorder='little').hex()

Target =0x0000ffff00000000000000000000000000000000000000000000000000000000
with open("coinbase_data.txt", "r") as file:
    data = [line.strip() for line in file]


def encode_varint(value):
    if value < 0xFD:
        return bytes([value])
    elif value <= 0xFFFF:
        return b'\xFD' + value.to_bytes(2, byteorder='little')
    elif value <= 0xFFFF_FFFF:
        return b'\xFE' + value.to_bytes(4, byteorder='little')
    else:
        return b'\xFF' + value.to_bytes(8, byteorder='little')
    
def bytes_to_compact_hex(bytes_data):
    return ''.join(format(byte, '02x') for byte in bytes_data)

merkle_root = data[0]
coinbase_tx = data[1]

nonce = 0
# while(True):
#     serial = "010000000000000000000000000000000000000000000000000000000000000000000000"
#     serial += merkle_root
#     serial += int_to_little_endian_hex(int(time.time()))
#     serial += "ffff001d"
#     serial += int_to_little_endian_hex(nonce)
#     serial += bytes_to_compact_hex(encode_varint(2669))
#     hash = int(hash256(serial), 16)
#     if(hash < Target):
#         print(hash, nonce, serial)
#         break
#     nonce+=1

print(coinbase_tx)