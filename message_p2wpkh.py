import json
import hashlib

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

def hash256(msg):
    hash = hashlib.sha256(hashlib.sha256(bytes.fromhex(msg)).digest()).digest()
    return hash.hex()

file = open(f'code-challenge-2024-rijul57/mempool/0aac26114009989817ba396fbfcdb0ab2f2a51a30df5d134d3294aacb27e8f69.json', 'r')                                                                                                    
data = file.read()
obj = json.loads(data)

temp1 = ""

for i in range(len(obj['vin'])):
    tx = obj['vin'][i]
    txid_little_endian = bytes.fromhex(tx['txid'])[::-1].hex()
    temp1 += txid_little_endian
    temp1 += tx['vout'].to_bytes(4, byteorder = 'little').hex()

temp2 = ""

for i in range(len(obj['vin'])):
    tx = obj['vin'][i]
    temp2 += tx['sequence'].to_bytes(4, byteorder = 'little').hex()

temp3 = ""

for i in range(len(obj['vout'])):
    tx = obj["vout"][i]
    temp3 += tx['value'].to_bytes(8, byteorder = 'little').hex()
    temp3 += bytes_to_compact_hex(encode_varint(len(tx['scriptpubkey'])//2))
    temp3 += tx['scriptpubkey']

info = []


for i in range(len(obj['vin'])):
    serial = ""
    if(str(obj['version']) == '1'):
        serial += "01000000"
    else:   
        serial += "02000000"
    serial += hash256(temp1)
    serial += hash256(temp2)
    tx = obj['vin'][i]
    txid_little_endian = bytes.fromhex(tx['txid'])[::-1].hex()
    serial += txid_little_endian
    serial += tx['vout'].to_bytes(4, byteorder = 'little').hex()
    serial += "1976a914"
    serial += tx['prevout']['scriptpubkey'][4:]
    serial += "88ac"
    serial += tx['prevout']['value'].to_bytes(8, byteorder = 'little').hex()
    serial += tx['sequence'].to_bytes(4, byteorder = 'little').hex()
    serial += hash256(temp3)
    serial += obj['locktime'].to_bytes(4, byteorder = 'little').hex()
    serial += "01000000"
    info.append(serial)

print(info)



 