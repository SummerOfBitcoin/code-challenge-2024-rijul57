import time
import hashlib
from txid import get_txid

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

def get_merkle_root(coinbase_serialization):
    with open("valid_tx.txt", "r") as file:
        valid_tx = [line.strip() for line in file]
    txid_list = [hash256(coinbase_serialization)]
    for filename in valid_tx:
        txid = get_txid(filename)
        txid_list.append(txid)
    print(txid_list)
    return merkleroot(txid_list)

def make_block(coinbase_serialization):
    nonce = 0
    merkle_root = get_merkle_root(coinbase_serialization)
    print(merkle_root)
    while(True):
        header = "200000000000000000000000000000000000000000000000000000000000000000000000"
        header += merkle_root
        header += int_to_little_endian_hex(int(time.time()))
        header += "ffff001f"
        header += int_to_little_endian_hex(nonce)
        hash = hash256(header)
        hash_little_endian = bytes.fromhex(hash)[::-1].hex()
        if(int(hash_little_endian, 16) < TARGET):
            return header
        nonce += 1
