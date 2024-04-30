import time
import hashlib

def hash256(msg):
    hashp = hashlib.sha256(hashlib.sha256(bytes.fromhex(msg)).digest()).digest()
    return hashp.hex()

def merkleroot(txid_list):
    n = len(txid_list)
    if(n == 1):
        return txid_list[0]

    result = []
    for i in range(0, n, 2):
        if(i == n - 1):
            concat = txid_list[i]+txid_list[i]
        else:
            concat = txid_list[i]+txid_list[i+1]
        result.append(hash256(concat))
    return merkleroot(result)

def int_to_little_endian_hex(num):
    return num.to_bytes(4, byteorder='little').hex()

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
    
TARGET =0x0000ffff00000000000000000000000000000000000000000000000000000000

with open("coinbase_data.txt", "r") as file:
    data = [line.strip() for line in file]

with open("txid.txt", "r") as file:
    tx_list = [line.strip() for line in file]

coinbase_txid = hash256(data[0])
mr_list = [coinbase_txid] + tx_list
merkle_root = merkleroot(mr_list)

nonce = 0
while(True):
    serial = "200000000000000000000000000000000000000000000000000000000000000000000000"
    serial += merkle_root
    serial += int_to_little_endian_hex(int(time.time()))
    serial += "ffff001f"
    serial += int_to_little_endian_hex(nonce)
    hash = hash256(serial)
    hash_little_endian = bytes.fromhex(hash)[::-1].hex()
    if(int(hash_little_endian, 16) < TARGET):
        with open("block_data.txt", "w") as file:
            file.write(str(serial) + "\n")
        break
    nonce += 1
