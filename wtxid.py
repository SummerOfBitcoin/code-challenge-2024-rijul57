import json
import hashlib

with open("valid_tx.txt", "r") as file:
    valid_tx = [line.strip() for line in file]

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

def wtxid_legacy(obj):
    serial = ""
    if(str(obj['version']) == '1'):
        serial += "01000000"
    else:   
        serial += "02000000"

    serial += bytes_to_compact_hex(encode_varint(len(obj['vin'])))

    for i in range(len(obj['vin'])):
        tx = obj['vin'][i]
        txid_little_endian = bytes.fromhex(tx['txid'])[::-1].hex()
        serial += txid_little_endian
        serial += tx['vout'].to_bytes(4, byteorder = 'little').hex()
        serial += bytes_to_compact_hex(encode_varint(len(tx['scriptsig'])//2))
        serial += tx['scriptsig']
        serial += tx['sequence'].to_bytes(4, byteorder = 'little').hex()
        
    serial += bytes_to_compact_hex(encode_varint(len(obj['vout']) ))

    for i in range(len(obj['vout'])):
        tx = obj["vout"][i]
        serial += tx['value'].to_bytes(8, byteorder = 'little').hex()
        serial += bytes_to_compact_hex(encode_varint(len(tx['scriptpubkey'])//2))
        serial += tx['scriptpubkey']
        
    serial += obj['locktime'].to_bytes(4, byteorder = 'little').hex()
    return hash256(serial)

def wtxid_segwit(obj):
    serial = ""
    if(str(obj['version']) == '1'):
        serial += "01000000"
    else:   
        serial += "02000000"

    serial += "0001"
    serial += bytes_to_compact_hex(encode_varint(len(obj['vin'])))

    for i in range(len(obj['vin'])):
        tx = obj['vin'][i]
        txid_little_endian = bytes.fromhex(tx['txid'])[::-1].hex()
        serial += txid_little_endian
        serial += tx['vout'].to_bytes(4, byteorder = 'little').hex()
        serial += bytes_to_compact_hex(encode_varint(len(tx['scriptsig'])//2))
        serial += tx['scriptsig']
        serial += tx['sequence'].to_bytes(4, byteorder = 'little').hex()
        
    serial += bytes_to_compact_hex(encode_varint(len(obj['vout']) ))

    for i in range(len(obj['vout'])):
        tx = obj["vout"][i]
        serial += tx['value'].to_bytes(8, byteorder = 'little').hex()
        serial += bytes_to_compact_hex(encode_varint(len(tx['scriptpubkey'])//2))
        serial += tx['scriptpubkey']

    for i in range(len(obj['vin'])):
        tx = obj['vin'][i]
        serial += "02"
        serial += bytes_to_compact_hex(encode_varint(len(tx['witness'][0])//2))
        serial += tx['witness'][0]
        serial += bytes_to_compact_hex(encode_varint(len(tx['witness'][1])//2))
        serial += tx['witness'][1]
    serial += obj['locktime'].to_bytes(4, byteorder = 'little').hex()
    return hash256(serial)

wtxid_list = []

for filename in valid_tx:
    file = open(f'code-challenge-2024-rijul57/mempool/{filename}', 'r')                                                                                                    
    data = file.read()
    obj = json.loads(data)

    isp2pkh = False
    if(obj['vin'][0]['prevout']['scriptpubkey_type'] == 'p2pkh'):
        isp2pkh=True

    if(isp2pkh):
        hash = wtxid_legacy(obj)
    else:
        hash = wtxid_segwit(obj)

    wtxid_list.append(hash)

with open("wtxid.txt", "w") as file:
    for item in wtxid_list:
        file.write(str(item) + "\n")